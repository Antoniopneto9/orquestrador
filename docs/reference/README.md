# Reference

Complete catalog of commands, agents, templates, and configuration.

## Slash Commands

### Workflow Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/brainstorm` | Explore ideas | Idea description or file path | `BRAINSTORM_{FEATURE}.md` |
| `/define` | Capture requirements | Brainstorm file, notes, or description | `DEFINE_{FEATURE}.md` |
| `/design` | Create architecture | DEFINE file path | `DESIGN_{FEATURE}.md` |
| `/build` | Execute implementation | DESIGN file path | `BUILD_REPORT_{FEATURE}.md` |
| `/ship` | Archive completed work | DEFINE file path | `SHIPPED_{DATE}.md` |
| `/iterate` | Update any phase document | File path plus change description | Updated artifact set |
| `/create-pr` | Create pull request | Optional title and flags | GitHub PR |

### Project Memory Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `/start-project` | Initialize project-memory artifacts | manifest, roadmap, current state, metrics |
| `/checkpoint` | Save operational checkpoint | checkpoint file plus refreshed current state |
| `/status` | Recover and summarize project state | concise status report with next-step guidance |
| `/forecast-week` | Estimate realistic next-week progress | executive report plus weekly metrics |

### Core Commands

| Command | Purpose | Input |
|---------|---------|-------|
| `/memory` | Save session insights to storage | Optional context note |
| `/sync-context` | Update `CLAUDE.md` from codebase | flags |
| `/readme-maker` | Generate `README.md` | flags |

### Knowledge Commands

| Command | Purpose |
|---------|---------|
| `/create-kb` | Create a KB domain |

### Review Commands

| Command | Purpose |
|---------|---------|
| `/review` | Dual AI code review |

## Agents

### Workflow Agents (6)

- `brainstorm-agent`
- `define-agent`
- `design-agent`
- `build-agent`
- `ship-agent`
- `iterate-agent`

### Operational Agents (5)

- `project-tracker-agent`
- `session-analyst-agent`
- `roadmap-guardian-agent`
- `weekly-forecaster-agent`
- `executive-status-agent`

### Code Quality Agents (4)

- `code-reviewer`
- `code-cleaner`
- `code-documenter`
- `test-generator`

### Communication Agents (4)

- `adaptive-explainer`
- `linear-project-manager`
- `meeting-analyst`
- `the-planner`

### Exploration Agents (2)

- `codebase-explorer`
- `kb-architect`

## Project Memory Files

| File | Purpose |
|------|---------|
| `.claude/project-memory/project-manifest.md` | project objective, idea, guardrails, workflow, suggested agents |
| `.claude/project-memory/roadmap.json` | areas, tasks, dependencies, progress |
| `.claude/project-memory/current-state.md` | live recovery context |
| `.claude/project-memory/checkpoints/` | timestamped checkpoints |
| `.claude/project-memory/sessions/` | optional detailed session logs |
| `.claude/project-memory/metrics/weekly-metrics.json` | weekly delivery and forecast metrics |
| `.claude/project-memory/metrics/progress-snapshot.json` | latest progress rollup |
| `.claude/project-memory/reports/executive-status.md` | management-friendly weekly report |

## Templates

### SDD Templates

- `.claude/sdd/templates/BRAINSTORM_TEMPLATE.md`
- `.claude/sdd/templates/DEFINE_TEMPLATE.md`
- `.claude/sdd/templates/DESIGN_TEMPLATE.md`
- `.claude/sdd/templates/BUILD_REPORT_TEMPLATE.md`
- `.claude/sdd/templates/SHIPPED_TEMPLATE.md`

### Project Memory Templates

- `.claude/project-memory/templates/manifest-template.md`
- `.claude/project-memory/templates/session-template.md`
- `.claude/project-memory/templates/checkpoint-template.md`
- `.claude/project-memory/templates/status-template.md`
- `.claude/project-memory/templates/forecast-template.md`
