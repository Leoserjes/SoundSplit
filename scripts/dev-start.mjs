import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export const DEFAULT_API_HOST = "127.0.0.1";
export const DEFAULT_API_PORT = "8000";
export const DEFAULT_DESKTOP_HOST = "127.0.0.1";
export const DEFAULT_DESKTOP_PORT = "1420";

export function resolveWorkspacePaths(workspaceRoot, platform = process.platform) {
  return {
    apiCwd: resolve(workspaceRoot, "apps", "api"),
    desktopCwd: workspaceRoot,
    pythonPath: resolve(
      workspaceRoot,
      ".venv",
      platform === "win32" ? "Scripts/python.exe" : "bin/python"
    )
  };
}

export function createChildEnv(baseEnv, overrides = {}, platform = process.platform) {
  const childEnv = {};
  const keysByLowercase = new Map();

  for (const [key, value] of Object.entries(baseEnv)) {
    if (value === undefined) {
      continue;
    }

    if (platform === "win32") {
      const lowercaseKey = key.toLowerCase();
      const existingKey = keysByLowercase.get(lowercaseKey);

      if (existingKey) {
        if (lowercaseKey === "path" && key === "Path") {
          delete childEnv[existingKey];
          keysByLowercase.set(lowercaseKey, key);
        } else {
          continue;
        }
      } else {
        keysByLowercase.set(lowercaseKey, key);
      }
    }

    childEnv[key] = String(value);
  }

  for (const [key, value] of Object.entries(overrides)) {
    if (value === undefined) {
      continue;
    }

    if (platform === "win32") {
      const lowercaseKey = key.toLowerCase();
      const existingKey = keysByLowercase.get(lowercaseKey);

      if (existingKey && existingKey !== key) {
        delete childEnv[existingKey];
      }

      keysByLowercase.set(lowercaseKey, key);
    }

    childEnv[key] = String(value);
  }

  return childEnv;
}

export function createProcessSpecs({
  env = process.env,
  platform = process.platform,
  workspaceRoot
}) {
  const paths = resolveWorkspacePaths(workspaceRoot, platform);
  const npmCommand = platform === "win32" ? env.ComSpec || "cmd.exe" : "npm";
  const npmArgsPrefix = platform === "win32" ? ["/d", "/s", "/c", "npm"] : [];
  const apiHost = env.API_HOST || DEFAULT_API_HOST;
  const apiPort = env.API_PORT || DEFAULT_API_PORT;
  const desktopHost = env.DESKTOP_HOST || DEFAULT_DESKTOP_HOST;
  const desktopPort = env.DESKTOP_PORT || DEFAULT_DESKTOP_PORT;
  const apiBaseUrl = env.VITE_API_BASE_URL || `http://${apiHost}:${apiPort}`;

  return [
    {
      args: [
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host",
        apiHost,
        "--port",
        apiPort
      ],
      command: paths.pythonPath,
      cwd: paths.apiCwd,
      env: createChildEnv(env, {
        API_HOST: apiHost,
        API_PORT: apiPort,
        SOUNDSPLIT_ENV: env.SOUNDSPLIT_ENV || "development"
      }, platform),
      label: "api",
      url: `http://${apiHost}:${apiPort}`
    },
    {
      args: [
        ...npmArgsPrefix,
        "--workspace",
        "apps/desktop",
        "run",
        "dev",
        "--",
        "--host",
        desktopHost,
        "--port",
        desktopPort,
        "--strictPort"
      ],
      command: npmCommand,
      cwd: paths.desktopCwd,
      env: createChildEnv(env, {
        VITE_API_BASE_URL: apiBaseUrl,
        VITE_API_ENVIRONMENT: env.VITE_API_ENVIRONMENT || "development"
      }, platform),
      label: "desktop",
      url: `http://${desktopHost}:${desktopPort}`
    }
  ];
}

export function isCliEntrypoint(importMetaUrl, argv = process.argv) {
  return argv[1] ? importMetaUrl === pathToFileURL(resolve(argv[1])).href : false;
}

function prefixOutput(label, stream, writer) {
  let pending = "";

  stream.on("data", (chunk) => {
    pending += chunk.toString();
    const lines = pending.split(/\r?\n/);
    pending = lines.pop() || "";

    for (const line of lines) {
      if (line.length > 0) {
        writer.write(`[${label}] ${line}\n`);
      }
    }
  });

  stream.on("end", () => {
    if (pending.length > 0) {
      writer.write(`[${label}] ${pending}\n`);
    }
  });
}

function stopChild(child) {
  if (!child.pid || child.killed) {
    return;
  }

  if (process.platform === "win32") {
    spawn("taskkill", ["/pid", String(child.pid), "/T", "/F"], {
      stdio: "ignore"
    });
    return;
  }

  child.kill("SIGTERM");
}

export function startDevProcesses(specs) {
  const children = [];
  let shuttingDown = false;

  function stopAll(exitCode = 0) {
    if (shuttingDown) {
      return;
    }

    shuttingDown = true;

    for (const child of children) {
      stopChild(child);
    }

    setTimeout(() => {
      process.exit(exitCode);
    }, 100);
  }

  for (const spec of specs) {
    const child = spawn(spec.command, spec.args, {
      cwd: spec.cwd,
      env: spec.env,
      stdio: ["inherit", "pipe", "pipe"]
    });

    children.push(child);
    prefixOutput(spec.label, child.stdout, process.stdout);
    prefixOutput(spec.label, child.stderr, process.stderr);

    child.on("exit", (code, signal) => {
      if (!shuttingDown) {
        const reason = signal ? `signal ${signal}` : `exit code ${code ?? 0}`;
        process.stderr.write(`[dev] ${spec.label} stopped with ${reason}. Stopping all services.\n`);
        stopAll(code ?? 1);
      }
    });
  }

  process.on("SIGINT", () => stopAll(0));
  process.on("SIGTERM", () => stopAll(0));

  return children;
}

export async function main() {
  const workspaceRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
  const specs = createProcessSpecs({ workspaceRoot });
  const apiSpec = specs.find((spec) => spec.label === "api");
  const desktopSpec = specs.find((spec) => spec.label === "desktop");

  if (!apiSpec || !existsSync(apiSpec.command)) {
    process.stderr.write(
      [
        "[dev] Missing Python virtual environment.",
        "[dev] Expected .venv Python at:",
        `[dev] ${apiSpec?.command}`,
        "[dev] Run: python -m venv .venv",
        "[dev] Then: .venv\\Scripts\\python.exe -m pip install -e apps\\api[test] -e workers\\ai[test]",
        ""
      ].join("\n")
    );
    process.exit(1);
  }

  process.stdout.write(
    [
      "SoundSplit local development",
      `API: ${apiSpec.url}`,
      `Desktop: ${desktopSpec?.url}`,
      "Press Ctrl+C to stop both processes.",
      ""
    ].join("\n")
  );

  startDevProcesses(specs);
}

if (isCliEntrypoint(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`[dev] ${error instanceof Error ? error.message : String(error)}\n`);
    process.exit(1);
  });
}
