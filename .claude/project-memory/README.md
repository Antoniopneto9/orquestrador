# Project Memory Extension

Operational memory layer for AgentSpec projects.

This extension complements Spec-Driven Development with persistent project tracking, session checkpoints, recovery context, and weekly forecasting. It is designed to live beside `.claude/sdd/` and reuse SDD artifacts instead of replacing them.

---

## Purpose

Use `.claude/project-memory/` to answer operational questions that the SDD pipeline alone does not keep current:

- Where is the project now?
- What changed this week?
- Which areas are on track or stalled?
- What decisions and blockers were recorded recently?
- Which command or agent should be used next?
- Is execution drifting away from the original project idea?

This layer is governed by `PROJECT_RULES.md` (highest precedence).

---

## Core Commands

| Command | When to Use | Primary Output |
|---------|-------------|----------------|
| `/start-project` | After `/design` or when initializing an existing project | `project-manifest.md`, `roadmap.json`, `current-state.md` |
| `/checkpoint` | During or at the end of a working session | `checkpoints/*.md`, updated `current-state.md` |
| `/status` | When resuming work or preparing an update | current state summary with next-step guidance |
| `/forecast-week` | Weekly planning and expectation setting | `reports/executive-status.md`, updated metrics |

---

## Folder Responsibilities

| Path | Purpose |
|------|---------|
| `project-manifest.md` | Original idea, objective, areas, guardrails, recommended workflow |
| `roadmap.json` | Structured execution plan with progress by area and task |
| `current-state.md` | Live operational summary for resuming work |
| `sessions/` | Optional detailed session logs |
| `checkpoints/` | Timestamped operational snapshots |
| `metrics/weekly-metrics.json` | Week-over-week delivery and forecast metrics |
| `metrics/progress-snapshot.json` | Latest progress rollup |
| `reports/executive-status.md` | Management-ready weekly status |
| `templates/` | Reusable templates for new projects and repeated updates |

---

## Integration Rules

Project Memory must read existing SDD artifacts whenever they exist:

1. Align `project-manifest.md` with the latest DEFINE artifact.
2. Derive roadmap tasks from DESIGN manifests and major decisions.
3. Reference BUILD reports in checkpoints and status summaries.
4. Use archive history to preserve continuity after `/ship`.
5. Keep guardrails visible so roadmap drift is detectable.
6. For materially completed tasks, keep `current-state.md`, checkpoints, and roadmap task status synchronized.

---

## Recommended Workflow

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
10. Review archive + project-memory reports for continuity
```

---

## How It Complements Existing Commands

| Existing Command | Project Memory Contribution |
|------------------|-----------------------------|
| `/brainstorm` | Captures the initial idea and guardrails in the project manifest |
| `/define` | Supplies objectives, success criteria, and non-goals |
| `/design` | Supplies execution areas, dependencies, and file/task breakdown |
| `/build` | Supplies completed work, touched files, and verification evidence |
| `/ship` | Preserves continuity into archive and future planning cycles |
| `/memory` | Saves high-signal insights; `/checkpoint` saves operational state |
| `/sync-context` | Keeps `CLAUDE.md` aligned with the evolving project memory state |

---

## Command Heuristics

- Use `/checkpoint` when the session changed project state.
- Use `/status` before touching code after a break.
- Use `/forecast-week` when planning work with deadlines or shared stakeholders.
- Use `roadmap-guardian-agent` whenever scope drift or competing asks appear.

---

## File Discipline

- Keep `current-state.md` concise and current.
- Store timestamps in ISO-like format with timezone when possible.
- Update both metrics files whenever progress materially changes.
- Treat guardrails as active constraints, not archive-only notes.
- Include `Compliance status: PASS/FAIL` in operational close-out responses.
