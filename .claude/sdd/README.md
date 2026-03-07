# AgentSpec

> **The AI-Native Specification and Project Memory Framework for Claude Code**
>
> *"From Specification to Specialized Execution with Operational Continuity"*

---

## Executive Summary

| Aspect | Details |
|--------|---------|
| **Project** | AgentSpec - Hybrid SDD plus Project Memory framework |
| **Tagline** | Spec-Driven Development with operational continuity |
| **Business Problem** | Teams lose both specification traceability and day-to-day execution context |
| **Solution** | 5-phase workflow plus project-memory layer for checkpoints, recovery, forecasting, and guardrails |
| **Target Audience** | AI-native teams using Claude Code and similar coding-agent workflows |
| **License** | MIT |

## What This Is

AgentSpec transforms requirements into working code with full traceability, then keeps the project operationally recoverable. It provides a structured 5-phase development workflow (`/brainstorm` -> `/define` -> `/design` -> `/build` -> `/ship`) plus a Project Memory layer for checkpoints, recovery context, forecasting, and scope drift detection.

## Hybrid Model

```text
Specification Stream: /brainstorm -> /define -> /design -> /build -> /ship
Operational Stream:                     /start-project -> /checkpoint -> /status -> /forecast-week
```

The two streams share the same source of truth. Project Memory reuses DEFINE, DESIGN, BUILD, and archive artifacts instead of duplicating them.

## Core Workflow

| Phase | Command | Primary Artifact | Operational Companion |
|-------|---------|------------------|-----------------------|
| 0 | `/brainstorm` | `BRAINSTORM_*.md` | guardrails and core idea for manifest |
| 1 | `/define` | `DEFINE_*.md` | objective, success criteria, non-goals |
| 2 | `/design` | `DESIGN_*.md` | roadmap areas, tasks, dependencies |
| Init | `/start-project` | `project-manifest.md`, `roadmap.json` | initializes project memory |
| 3 | `/build` | code + `BUILD_REPORT_*.md` | checkpoint evidence and progress updates |
| Live | `/checkpoint` | `checkpoints/*.md` | session capture and state refresh |
| Live | `/status` | recovery summary | current progress and next-step guidance |
| Live | `/forecast-week` | `executive-status.md` | planning and expectation setting |
| 4 | `/ship` | archived artifacts + `SHIPPED_*.md` | continuity for future planning |

## Key Directories

```text
.claude/
|-- sdd/                 # Spec-Driven Development stream
|-- project-memory/      # Operational memory stream
|-- agents/              # Workflow, operational, quality, communication, exploration agents
|-- commands/            # Workflow, project-memory, core, review, knowledge commands
`-- kb/                  # Curated knowledge domains
```

## Why Project Memory Exists

SDD captures why and how a feature should be built. Project Memory captures how execution is actually progressing over time.

Use it to answer:

- Where is the project now?
- Which roadmap areas are advancing?
- What changed in the latest session?
- What should happen next?
- Are we drifting away from the original idea?

## Recommended Flow

```text
1. /brainstorm
2. /define
3. /design
4. /start-project
5. /build
6. /checkpoint during execution
7. /status when resuming
8. /forecast-week for planning
9. /ship
10. Review archive and project-memory reports for continuity
```

## References

| Resource | Location |
|----------|----------|
| SDD Index | `.claude/sdd/_index.md` |
| Commands | `.claude/commands/README.md` |
| Agents | `.claude/agents/README.md` |
| Project Memory | `.claude/project-memory/README.md` |
