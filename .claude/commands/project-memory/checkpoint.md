---
name: checkpoint
description: Save an operational checkpoint for the current work session
---

# Checkpoint Command

> Record what changed in the current session and update the live project state.

## Usage

```bash
/checkpoint
/checkpoint "Finished API authentication handlers and updated tests"
```

## What It Does

1. Inspects current project state
2. Summarizes work in progress and recently completed work
3. Records files changed when available
4. Captures:
   - session summary
   - tasks completed
   - decisions taken
   - blockers
   - next steps
5. Updates `.claude/project-memory/current-state.md`
6. Writes a timestamped file to `.claude/project-memory/checkpoints/`
7. Optionally writes a richer session log to `.claude/project-memory/sessions/`

---

## Source Inputs

```markdown
Read(PROJECT_RULES.md)
Read(.claude/project-memory/project-manifest.md)
Read(.claude/project-memory/roadmap.json)
Read(.claude/project-memory/current-state.md)
Glob(.claude/project-memory/checkpoints/*.md)

Optional:
Read(.claude/sdd/reports/BUILD_REPORT_{FEATURE}.md)
Read(.claude/sdd/features/DESIGN_{FEATURE}.md)
Git diff / changed files summary when available
```

---

## Process

### Step 1: Summarize Session

Use `session-analyst-agent` logic:

- what work happened
- what tasks were completed
- what changed in files or configuration
- which decisions matter later
- which blockers remain

### Step 2: Map Work to Roadmap

Use `project-tracker-agent` logic:

- map completed work to roadmap tasks
- adjust area progress
- update progress snapshot if needed
- move applicable tasks from `todo` or `in_progress` to `done`

### Step 3: Run Drift Check

Use `roadmap-guardian-agent` logic:

- compare current execution to original idea
- note drift risk or guardrail violations

### Step 4: Persist the Checkpoint

Create:

```text
.claude/project-memory/checkpoints/CHECKPOINT_{YYYY-MM-DD}_{HHMM}.md
```

Update:

- `.claude/project-memory/current-state.md`
- `.claude/project-memory/metrics/progress-snapshot.json`

---

## Output Shape

Checkpoint must include:

- summary
- worked on
- files changed
- tasks completed
- decisions taken
- blockers
- next steps
- drift check
- recommended commands
- recommended agents

---

## Quality Gate

```text
[ ] Session summary is concise and specific
[ ] Completed tasks map to roadmap areas
[ ] Decisions include rationale
[ ] Blockers are explicit, not implied
[ ] Next steps are executable
[ ] Drift check is recorded
[ ] Roadmap task statuses are synchronized when completion evidence exists
[ ] Close-out includes "Compliance status: PASS/FAIL"
```

---

## Compliance Gate

`/checkpoint` MUST enforce `PROJECT_RULES.md`.

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

If checkpoint or state update is missing, mark `Compliance status: FAIL`.

---

## References

- Rules: `PROJECT_RULES.md`
- Template: `.claude/project-memory/templates/checkpoint-template.md`
- State file: `.claude/project-memory/current-state.md`
- Related command: `.claude/commands/project-memory/status.md`
