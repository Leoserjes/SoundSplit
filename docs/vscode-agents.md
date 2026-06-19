# VS Code Agents

SoundSplit includes workspace custom agents for VS Code's Agents window.

## Available Agents

- Ada: Engineering Manager
- Maestro: Product Manager
- Turing: Backend Developer
- Pixel: Front-End Developer
- Grace: QA
- Linus: Release Coordinator
- Atlas: Agent Manager

The agent files live in `.github/agents/*.agent.md`, which VS Code discovers as workspace custom agents.

## Open The Agents Window

Use any of these options:

- Run `code --agents` from a terminal.
- In VS Code, run `Chat: Open Agents Window` from the Command Palette.
- In VS Code, run the task `Open VS Code Agents Window`.
- Select `Open in Agents` from the VS Code title bar when available.

After the Agents window opens, start a new session for this workspace and select one of the SoundSplit custom agents from the agent/customization picker.

## Suggested Delivery Flow

For feature work, start with Atlas to coordinate ownership, then hand off through the repo delivery loop:

```text
Atlas -> Maestro -> Ada -> Turing/Pixel -> Grace -> Linus -> Atlas
```

Implementation cards should use separate agent sessions for the implementing developer and Grace QA. The developer session moves the card to `QA` with a handoff; Grace either returns it to `In Progress` with findings or moves it forward with a QA handoff. Linus should only run release review after that QA evidence exists.

Each custom agent includes handoff buttons for common next steps.

## Validation Tasks

The workspace includes VS Code tasks for the current quality gates:

- `Validate: desktop build`
- `Validate: desktop tests`
- `Validate: backend and worker tests`
- `Validate: Python compile`

These tasks mirror the commands documented in `docs/quality-gates.md`.
