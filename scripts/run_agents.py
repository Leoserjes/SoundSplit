#!/usr/bin/env python3
"""SoundSplit Continuous Autonomous Multi-Agent Runner

Autonomous AI agents that execute sprint tasks sequentially and continuously.
Powered by Google Gemini (google-genai) with tool execution and GitHub Issue tracking.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    print("Error: Missing rich. Run: pip install rich")
    sys.exit(1)

console = Console(force_terminal=True, legacy_windows=False)
ROOT_DIR = Path(__file__).resolve().parent.parent

AGENT_PERSONAS = {
    "Ada": {
        "role": "Engineering Manager (EM)",
        "color": "cyan",
        "system": """You are Ada, Engineering Manager (EM) at SoundSplit.
You own architecture decisions, schemas, and system standards.
Inspect the codebase, write clear architecture specifications into docs/architecture.md, and ensure all system contracts and boundaries are robust.""",
    },
    "Turing": {
        "role": "Backend Developer",
        "color": "green",
        "system": """You are Turing, Backend Developer at SoundSplit.
You implement FastAPI endpoints, data models, repository layers, and storage adapters in apps/api and workers/ai.
You MUST write thorough pytest unit tests for every backend feature in apps/api/tests/ or workers/ai/tests/.
You must run pytest using run_shell_command and ensure all tests pass before considering a task complete.""",
    },
    "Pixel": {
        "role": "Front-End Developer",
        "color": "magenta",
        "system": """You are Pixel, Front-End Developer at SoundSplit.
You implement desktop/frontend features in apps/desktop using React, TypeScript, and Vite.
You MUST write unit tests using Vitest (src/**/*.test.tsx/ts) and verify that `npm run desktop:test` and `npm run desktop:build` pass before completing your task.""",
    },
    "Grace": {
        "role": "QA Engineer",
        "color": "yellow",
        "system": """You are Grace, QA Engineer at SoundSplit.
You review developer tests, identify untested edge cases, write integration/regression test suites, and audit security and data safety boundaries.
You run the full test suite and verify quality gates.""",
    },
    "Linus": {
        "role": "Release Coordinator",
        "color": "blue",
        "system": """You are Linus, Release Coordinator at SoundSplit.
You prepare release documentation in docs/releases/, verify all quality gates pass, and assemble release checklists.""",
    },
}


class AgentTools:
    """Tools executable by the LLM agents."""

    @staticmethod
    def read_file(path: str) -> str:
        """Read the text contents of a file relative to the repository root."""
        target = ROOT_DIR / path
        if not target.exists():
            return f"Error: File '{path}' does not exist."
        return target.read_text(encoding="utf-8")

    @staticmethod
    def write_file(path: str, content: str) -> str:
        """Write or overwrite a file with given text content."""
        target = ROOT_DIR / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} bytes to '{path}'."

    @staticmethod
    def replace_in_file(path: str, target: str, replacement: str) -> str:
        """Replace an exact block of text in a file with new text."""
        file_path = ROOT_DIR / path
        if not file_path.exists():
            return f"Error: File '{path}' does not exist."
        content = file_path.read_text(encoding="utf-8")
        if target not in content:
            return f"Error: Target text not found in '{path}'."
        updated = content.replace(target, replacement, 1)
        file_path.write_text(updated, encoding="utf-8")
        return f"Successfully replaced target in '{path}'."

    @staticmethod
    def list_directory(path: str = ".") -> str:
        """List files and directories in a given path."""
        target = ROOT_DIR / path
        if not target.exists():
            return f"Error: Path '{path}' does not exist."
        entries = []
        for item in sorted(target.iterdir()):
            kind = "DIR " if item.is_dir() else "FILE"
            entries.append(f"{kind} {item.name}")
        return "\n".join(entries) if entries else "(empty directory)"

    @staticmethod
    def run_shell_command(command: str) -> str:
        """Run a shell command (e.g. pytest, npm test, tsc) and return output."""
        try:
            res = subprocess.run(
                command,
                shell=True,
                cwd=str(ROOT_DIR),
                capture_output=True,
                text=True,
                timeout=120,
            )
            output = ""
            if res.stdout:
                output += f"STDOUT:\n{res.stdout}\n"
            if res.stderr:
                output += f"STDERR:\n{res.stderr}\n"
            output += f"Exit Code: {res.returncode}"
            return output
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 120 seconds."
        except Exception as e:
            return f"Error running command: {e}"

    @staticmethod
    def comment_github_issue(issue_number: int, body: str) -> str:
        """Post a comment or handoff report to a GitHub Issue."""
        cmd = f'gh issue comment {issue_number} --repo Leoserjes/SoundSplit --body "{body}"'
        res = subprocess.run(cmd, shell=True, cwd=str(ROOT_DIR), capture_output=True, text=True)
        return res.stdout or res.stderr or "Comment posted."

    @staticmethod
    def close_github_issue(issue_number: int, comment: str) -> str:
        """Close a completed GitHub Issue with a summary comment."""
        cmd = f'gh issue close {issue_number} --repo Leoserjes/SoundSplit --comment "{comment}"'
        res = subprocess.run(cmd, shell=True, cwd=str(ROOT_DIR), capture_output=True, text=True)
        return res.stdout or res.stderr or "Issue closed."


GEMINI_TOOL_FUNCTIONS = [
    AgentTools.read_file,
    AgentTools.write_file,
    AgentTools.replace_in_file,
    AgentTools.list_directory,
    AgentTools.run_shell_command,
    AgentTools.comment_github_issue,
    AgentTools.close_github_issue,
]


async def run_gemini_agent(
    agent_name: str,
    task_description: str,
    issue_number: int | None = None,
    max_steps: int = 15,
    model_name: str = "gemini-3.6-flash",
) -> str:
    """Runs a single autonomous agent on a specific task."""
    from google import genai
    from google.genai import types

    persona = AGENT_PERSONAS.get(agent_name, {
        "role": "Software Engineer",
        "color": "white",
        "system": "You are an AI software engineer at SoundSplit."
    })
    role_title = f"{agent_name} ({persona['role']})"
    color = persona.get("color", "white")

    console.print(Panel(
        f"[bold {color}]Starting {role_title}[/bold {color}]\n"
        f"Task: {task_description}\n"
        f"Issue: #{issue_number if issue_number else 'N/A'}\n"
        f"Engine: Google Gemini ({model_name})",
        title=f"Agent Worker [{agent_name}]",
        border_style=color
    ))

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]Error: GEMINI_API_KEY is not set in environment or .env file.[/bold red]")
        return "Missing GEMINI_API_KEY."

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        system_instruction=persona["system"],
        tools=GEMINI_TOOL_FUNCTIONS,
        temperature=0.2,
    )

    chat = client.chats.create(model=model_name, config=config)
    prompt = f"Task: {task_description}\nIssue Number: {issue_number}\nPlease solve this task autonomously using your available tools. Write code, execute tests with run_shell_command, and verify your changes before finishing."

    console.print(f"[{color}][{agent_name}] Analyzing task and executing steps...[/{color}]")

    response = None
    for attempt in range(1, 6):
        try:
            response = await asyncio.to_thread(chat.send_message, prompt)
            break
        except Exception as err:
            err_str = str(err)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                wait_time = 20 * attempt
                console.print(f"[{color}][{agent_name}] Rate limit reached. Throttling {wait_time}s before retry (attempt {attempt}/5)...[/{color}]")
                await asyncio.sleep(wait_time)
            else:
                raise err

    if not response:
        return f"{role_title} failed after retries."

    if response.text:
        console.print(f"[{color}][{agent_name}]: {response.text[:300]}...[/{color}]")

    console.print(f"[bold {color}][OK] {role_title} completed the task![/bold {color}]")
    return response.text or "Task completed."


def fetch_open_github_issues() -> list[dict]:
    """Fetches open GitHub issues for SoundSplit."""
    cmd = 'gh issue list --repo Leoserjes/SoundSplit --state open --json number,title,body --limit 30'
    res = subprocess.run(cmd, shell=True, cwd=str(ROOT_DIR), capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout:
        return []
    try:
        issues = json.loads(res.stdout)
        # Sort by issue number ascending
        return sorted(issues, key=lambda x: x.get("number", 0))
    except Exception:
        return []


def determine_owner_from_issue(issue: dict) -> str:
    """Detects which agent owns an issue from title or body."""
    title = issue.get("title", "")
    body = issue.get("body", "")
    for name in ["Turing", "Pixel", "Grace", "Ada", "Linus"]:
        if name.lower() in body.lower() or name.lower() in title.lower():
            return name
    # Default heuristics
    if "SS4-005" in title or "Desktop" in title or "Frontend" in title:
        return "Pixel"
    if "SS4-006" in title or "SS4-007" in title or "QA" in title or "Safety" in title:
        return "Grace"
    if "SS4-008" in title or "Release" in title:
        return "Linus"
    return "Turing"


async def run_autonomous_sprint_queue(model_name: str = "gemini-3.6-flash"):
    """Continuously runs open sprint issues autonomously one by one."""
    console.print(Panel.fit(
        "[bold cyan]SoundSplit Continuous Autonomous Agent Runtime[/bold cyan]\n"
        "Pulling live sprint issues from GitHub and executing backlog...",
        border_style="cyan"
    ))

    open_issues = fetch_open_github_issues()
    if not open_issues:
        console.print("[bold yellow]No open GitHub issues found. Backlog is clear![/bold yellow]")
        return

    console.print(f"[bold green]Found {len(open_issues)} open issues in backlog.[/bold green]")

    for issue in open_issues:
        num = issue["number"]
        title = issue["title"]
        owner = determine_owner_from_issue(issue)

        console.print(f"\n[bold white]==================================================[/bold white]")
        console.print(f"[bold cyan]Dispatching Issue #{num}: {title} to Agent {owner}[/bold cyan]")
        console.print(f"[bold white]==================================================[/bold white]")

        task_prompt = f"Implement Issue #{num}: {title}\nDetails:\n{issue.get('body', '')}\nPlease read the codebase, make the necessary modifications, run pytest or vitest to verify all tests pass, and comment your handoff on the issue."

        await run_gemini_agent(
            agent_name=owner,
            task_description=task_prompt,
            issue_number=num,
            model_name=model_name,
        )

        console.print("[yellow]Cooling down for 15s before picking up the next issue...[/yellow]")
        await asyncio.sleep(15)

    console.print(Panel.fit("[bold green]All sprint backlog issues have been processed autonomously![/bold green]", border_style="green"))


def main():
    parser = argparse.ArgumentParser(description="SoundSplit Autonomous Multi-Agent Runner")
    parser.add_argument("--agent", choices=["Ada", "Turing", "Pixel", "Grace", "Linus"], help="Run a specific agent")
    parser.add_argument("--task", help="Custom task description for the agent")
    parser.add_argument("--issue", type=int, help="GitHub Issue number")
    parser.add_argument("--queue", action="store_true", help="Run through all open GitHub issues in queue")
    parser.add_argument("--model", default="gemini-3.6-flash", help="Gemini model identifier")

    args = parser.parse_args()

    if args.agent and args.task:
        asyncio.run(run_gemini_agent(
            agent_name=args.agent,
            task_description=args.task,
            issue_number=args.issue,
            model_name=args.model,
        ))
    else:
        # Default: Process open sprint queue continuously
        asyncio.run(run_autonomous_sprint_queue(model_name=args.model))


if __name__ == "__main__":
    main()
