<div align="center">

# AgentSpec

## Spec-Driven Development with Project Memory

Turn ideas into shipped features through a structured AI workflow that also preserves roadmap, checkpoints, recovery context, and weekly planning.

[Quick Start](#quick-start) | [Documentation](docs/) | [Project Memory](.claude/project-memory/README.md) | [Contributing](CONTRIBUTING.md)

</div>

---

## What Changed

AgentSpec now operates as a hybrid framework:

1. Spec-Driven Development for turning ideas into architecture and delivery.
2. Project Memory for tracking execution state over time.

The original 5-phase workflow remains intact. The new operational layer adds project initialization, session checkpoints, context recovery, weekly forecasting, and scope guardrails.

In Claude Code these capabilities are exposed as slash commands. In other coding-agent environments, the same files and command documents can be followed procedurally as an operating playbook.

## Governance Source of Truth

Operational documentation enforcement is policy-based and centralized in [PROJECT_RULES.md](PROJECT_RULES.md).

Rule precedence:

1. `PROJECT_RULES.md`
2. `.claude/project-memory/README.md`
3. Command and agent files

## Core Workflow

```text
/brainstorm -> /define -> /design -> /start-project -> /build
             -> /checkpoint -> /status -> /forecast-week -> /ship
```

## Project Memory Layer

The new layer lives in `.claude/project-memory/` and provides:

- `project-manifest.md` for objective, idea, guardrails, and workflow guidance
- `roadmap.json` for areas, tasks, dependencies, and progress
- `current-state.md` for recovery-ready context
- `checkpoints/` and `sessions/` for operational history
- `metrics/` and `reports/` for forecasting and executive summaries

## New Commands

| Command | Purpose |
|---------|---------|
| `/start-project` | Initialize the project-memory structure |
| `/checkpoint` | Save session progress, decisions, blockers, and next steps |
| `/status` | Recover current state and recommend next actions |
| `/forecast-week` | Estimate next-week progress and write executive reporting output |

## New Agents

| Agent | Purpose |
|-------|---------|
| `project-tracker-agent` | Keep roadmap and progress aligned |
| `session-analyst-agent` | Summarize working sessions |
| `roadmap-guardian-agent` | Detect scope drift and guardrail violations |
| `weekly-forecaster-agent` | Produce realistic weekly forecasts |
| `executive-status-agent` | Write management-friendly status reports |

## Quick Start

```bash
# 1. Explore the idea
claude> /brainstorm "Add user authentication with JWT"

# 2. Capture requirements
claude> /define USER_AUTH

# 3. Design the architecture
claude> /design USER_AUTH

# 4. Initialize the operational memory layer
claude> /start-project "User Authentication"

# 5. Build
claude> /build USER_AUTH

# 6. Save checkpoints during execution
claude> /checkpoint

# 7. Recover context when resuming
claude> /status

# 8. Forecast the next week
claude> /forecast-week

# 9. Ship with continuity preserved
claude> /ship USER_AUTH
```

## Project Structure

```text
.claude/
|-- agents/
|-- commands/
|-- sdd/
|-- project-memory/
`-- kb/
```

## Documentation

- [Getting Started](docs/getting-started/)
- [Core Concepts](docs/concepts/)
- [Reference](docs/reference/)
- [Project Memory README](.claude/project-memory/README.md)
- [Project Rules](PROJECT_RULES.md)
