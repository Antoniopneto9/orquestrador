# AgentSpec Commands

Slash commands for the hybrid AgentSpec workflow.

## Workflow Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `/brainstorm` | 0 | Explore ideas through dialogue |
| `/define` | 1 | Capture requirements |
| `/design` | 2 | Create architecture |
| `/build` | 3 | Execute implementation |
| `/ship` | 4 | Archive completed feature |
| `/iterate` | Any | Update documents mid-stream |
| `/create-pr` | Any | Create pull request |

## Project Memory Commands

| Command | Description |
|---------|-------------|
| `/start-project` | Initialize `.claude/project-memory/` from the project idea and SDD artifacts |
| `/checkpoint` | Save a timestamped operational checkpoint and refresh current state |
| `/status` | Recover context, summarize progress, and recommend the next action |
| `/forecast-week` | Generate a realistic next-week forecast and executive status report |

## Core Commands

| Command | Description |
|---------|-------------|
| `/memory` | Save high-signal session insights |
| `/sync-context` | Update `CLAUDE.md` |
| `/readme-maker` | Generate README |

## Knowledge Commands

| Command | Description |
|---------|-------------|
| `/create-kb` | Create KB domain |

## Review Commands

| Command | Description |
|---------|-------------|
| `/review` | Code review workflow |

## Recommended Hybrid Flow

```bash
claude> /brainstorm "Add user authentication with JWT"
claude> /define USER_AUTH
claude> /design USER_AUTH
claude> /start-project "User Authentication"
claude> /build USER_AUTH
claude> /checkpoint
claude> /status
claude> /forecast-week
claude> /ship USER_AUTH
```

## Usage

Commands are invoked in Claude Code:

```bash
claude> /define USER_AUTH
```
