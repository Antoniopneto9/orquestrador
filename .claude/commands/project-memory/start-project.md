---
name: start-project
description: Initialize the Project Memory layer for a new or existing project
---

# Start Project Command

> Create `.claude/project-memory/` and seed it from the project's idea, DEFINE, and DESIGN artifacts.

## Usage

```bash
/start-project "<project name>"
/start-project "<project name>" --objective "..." --areas "API, Data, UX" --guardrails "No rewrite, no paid SaaS"
```

## What It Does

1. Creates `.claude/project-memory/` if missing
2. Loads context from:
   - `.claude/sdd/features/DEFINE_*.md` when available
   - `.claude/sdd/features/DESIGN_*.md` when available
   - `CLAUDE.md`
   - direct user input
3. Generates:
   - `project-manifest.md`
   - `roadmap.json`
   - `current-state.md`
   - `metrics/weekly-metrics.json`
   - `metrics/progress-snapshot.json`
4. Stores:
   - original project idea
   - objective
   - areas of work
   - guardrails and non-goals
   - suggested commands and agents

---

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Project name | Yes | Canonical project label |
| Objective | No | Derive from DEFINE if omitted |
| Areas of work | No | Derive from DESIGN sections or manifest if omitted |
| Guardrails / non-goals | No | Derive from DEFINE out-of-scope and user notes |

---

## Process

### Step 1: Gather Source of Truth

```markdown
Read(PROJECT_RULES.md)
Read(.claude/project-memory/templates/manifest-template.md)
Read(.claude/project-memory/templates/status-template.md)
Read(CLAUDE.md)

Optional:
Read(.claude/sdd/features/DEFINE_{FEATURE}.md)
Read(.claude/sdd/features/DESIGN_{FEATURE}.md)
Read(.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md)
```

### Step 2: Build Initial Manifest

Populate:

- Project Name
- Objective
- Core Idea
- Success Criteria
- Areas of Work
- Guardrails
- Non-Goals
- Recommended Workflow
- Suggested Agents

### Step 3: Derive Initial Roadmap

Create `roadmap.json` with:

- top-level project metadata
- areas
- task list per area
- progress defaults
- dependencies
- notes grounded in DEFINE and DESIGN
- task status fields ready for lifecycle sync (`todo` -> `in_progress` -> `done`)

### Step 4: Seed Current State and Metrics

- `current-state.md` starts with project objective, active focus, pending tasks, and next best action
- `weekly-metrics.json` starts with zero or baseline values
- `progress-snapshot.json` captures the initial progress rollup

---

## Output

| Artifact | Location |
|----------|----------|
| Project manifest | `.claude/project-memory/project-manifest.md` |
| Roadmap | `.claude/project-memory/roadmap.json` |
| Current state | `.claude/project-memory/current-state.md` |
| Metrics | `.claude/project-memory/metrics/*.json` |

**Next Step:** `/build` if implementation is ready, or `/checkpoint` after the first working session.

---

## Quality Gate

Before finishing:

```text
[ ] Objective is explicit
[ ] Core idea is preserved from the original project brief
[ ] Areas of work are practical and non-overlapping
[ ] Guardrails and non-goals are documented
[ ] Roadmap tasks are concrete enough to track
[ ] Suggested commands and agents fit the current project stage
[ ] Rule precedence and compliance expectations are visible in outputs
```

---

## Compliance Gate

Before finalizing `/start-project`:

```text
[ ] PROJECT_RULES.md has been read
[ ] Rule precedence is explicitly respected
[ ] Bootstrap protocol is documented for future sessions
[ ] Operational output includes "Compliance status: PASS/FAIL"
```

Required close-out block:

```markdown
## Task Completion Record
- What was done: ...
- Files changed: ...
- Decisions: ...
- Blockers: ...
- Next steps: ...
- Evidence of updates:
  - current-state: ...
  - checkpoint: ...
  - roadmap status sync: ...
- Compliance status: PASS/FAIL
```

---

## References

- Rules: `PROJECT_RULES.md`
- Project memory: `.claude/project-memory/README.md`
- Template: `.claude/project-memory/templates/manifest-template.md`
- Related commands: `.claude/commands/project-memory/checkpoint.md`, `.claude/commands/project-memory/status.md`
