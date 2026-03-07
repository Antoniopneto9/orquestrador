# AgentSpec

> 5-phase Spec-Driven Development with Project Memory for operational continuity.

---

## Overview

AgentSpec now provides two integrated layers:

| Layer | Purpose |
|-------|---------|
| **SDD** | Convert ideas into shipped features through a structured five-phase workflow |
| **Project Memory** | Keep project state recoverable through checkpoints, status recovery, and forecasting |

## The Hybrid Pipeline

```text
Phase 0   Phase 1   Phase 2        Init            Phase 3        Live Ops             Phase 4
/brainstorm -> /define -> /design -> /start-project -> /build -> /checkpoint -> /status -> /forecast-week -> /ship
```

`/iterate` can still be used at any point to update the specification stream. Project Memory should then be refreshed through `/checkpoint` or `/status`.

## Commands

| Command | Purpose |
|---------|---------|
| `/brainstorm` | Explore the idea |
| `/define` | Capture and validate requirements |
| `/design` | Create architecture and file manifest |
| `/start-project` | Initialize project-memory artifacts |
| `/build` | Execute implementation |
| `/checkpoint` | Save a session checkpoint |
| `/status` | Recover current project state |
| `/forecast-week` | Estimate realistic next-week progress |
| `/ship` | Archive completed work |
| `/iterate` | Update spec artifacts mid-stream |

## Artifact Map

| Artifact | Location |
|----------|----------|
| Spec artifacts | `.claude/sdd/features/`, `.claude/sdd/reports/`, `.claude/sdd/archive/` |
| Operational artifacts | `.claude/project-memory/` |
| Agents | `.claude/agents/` |
| Commands | `.claude/commands/` |
| KB domains | `.claude/kb/` |

## Recommended Flow

```bash
/brainstorm "Build a user notification system"
/define USER_NOTIFICATIONS
/design USER_NOTIFICATIONS
/start-project "User Notifications"
/build USER_NOTIFICATIONS
/checkpoint
/status
/forecast-week
/ship USER_NOTIFICATIONS
```

## References

- Commands: `.claude/commands/README.md`
- Agents: `.claude/agents/README.md`
- Project Memory: `.claude/project-memory/README.md`
- Contracts: `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
