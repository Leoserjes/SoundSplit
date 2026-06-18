import assert from "node:assert/strict";
import { resolve } from "node:path";
import { describe, it } from "node:test";
import { pathToFileURL } from "node:url";

import {
  createChildEnv,
  createProcessSpecs,
  DEFAULT_API_HOST,
  DEFAULT_API_PORT,
  DEFAULT_DESKTOP_HOST,
  DEFAULT_DESKTOP_PORT,
  isCliEntrypoint,
  resolveWorkspacePaths
} from "./dev-start.mjs";

describe("dev-start", () => {
  it("resolves the Windows virtual environment Python path", () => {
    const paths = resolveWorkspacePaths("C:\\repo", "win32");

    assert.equal(paths.pythonPath, "C:\\repo\\.venv\\Scripts\\python.exe");
    assert.equal(paths.apiCwd, "C:\\repo\\apps\\api");
  });

  it("uses the existing local API and desktop ports by default", () => {
    const specs = createProcessSpecs({
      env: {},
      platform: "win32",
      workspaceRoot: "C:\\repo"
    });
    const api = specs.find((spec) => spec.label === "api");
    const desktop = specs.find((spec) => spec.label === "desktop");

    assert.equal(api.url, `http://${DEFAULT_API_HOST}:${DEFAULT_API_PORT}`);
    assert.equal(desktop.command, "cmd.exe");
    assert.deepEqual(desktop.args.slice(0, 4), ["/d", "/s", "/c", "npm"]);
    assert.equal(desktop.url, `http://${DEFAULT_DESKTOP_HOST}:${DEFAULT_DESKTOP_PORT}`);
    assert.equal(desktop.env.VITE_API_BASE_URL, `http://${DEFAULT_API_HOST}:${DEFAULT_API_PORT}`);
    assert.equal(desktop.env.VITE_API_ENVIRONMENT, "development");
  });

  it("sanitizes duplicate Windows environment keys before spawning children", () => {
    const env = createChildEnv(
      {
        PATH: "old-path",
        Path: "preferred-path",
        TEMP: "tmp",
        UNDEFINED_VALUE: undefined
      },
      {
        PATH: "override-path"
      },
      "win32"
    );

    assert.equal(env.PATH, "override-path");
    assert.equal(env.Path, undefined);
    assert.equal(env.TEMP, "tmp");
    assert.equal(Object.hasOwn(env, "UNDEFINED_VALUE"), false);
  });

  it("preserves configured API and desktop environment values", () => {
    const specs = createProcessSpecs({
      env: {
        API_HOST: "0.0.0.0",
        API_PORT: "8010",
        DESKTOP_HOST: "localhost",
        DESKTOP_PORT: "1430",
        SOUNDSPLIT_ENV: "staging",
        VITE_API_BASE_URL: "https://api.example.test",
        VITE_API_ENVIRONMENT: "staging"
      },
      platform: "linux",
      workspaceRoot: "C:\\repo"
    });
    const api = specs.find((spec) => spec.label === "api");
    const desktop = specs.find((spec) => spec.label === "desktop");

    assert.equal(api.command, resolve("C:\\repo", ".venv", "bin", "python"));
    assert.equal(api.url, "http://0.0.0.0:8010");
    assert.equal(api.env.SOUNDSPLIT_ENV, "staging");
    assert.equal(desktop.command, "npm");
    assert.equal(desktop.url, "http://localhost:1430");
    assert.equal(desktop.env.VITE_API_BASE_URL, "https://api.example.test");
    assert.equal(desktop.env.VITE_API_ENVIRONMENT, "staging");
  });

  it("detects the CLI entrypoint from argv", () => {
    assert.equal(isCliEntrypoint("file:///repo/scripts/dev-start.mjs", ["node"]), false);
    const entrypoint = resolve("scripts", "dev-start.mjs");
    assert.equal(isCliEntrypoint(pathToFileURL(entrypoint).href, ["node", entrypoint]), true);
  });
});
