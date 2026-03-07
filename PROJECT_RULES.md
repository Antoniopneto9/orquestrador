# Project Rules

Normative governance for operational documentation in AgentSpec.

## Rule Precedence

When rules conflict, use this precedence order:

1. `PROJECT_RULES.md` (this file)
2. `.claude/project-memory/README.md`
3. Individual command and agent files

## Mandatory Rules

The following are mandatory requirements:

- Every materially completed task MUST update `.claude/project-memory/current-state.md`.
- Every materially completed task MUST generate a checkpoint in `.claude/project-memory/checkpoints/`.
- Any relevant roadmap task in `.claude/project-memory/roadmap.json` MUST move from `todo` or `in_progress` to `done` when completion evidence exists.
- If a task is not materially complete, it MUST NOT be marked as `done`.
- Operational outputs MUST include `Compliance status: PASS` or `Compliance status: FAIL` before the task is considered closed.

## Session Bootstrap Protocol

At the start of any new chat/session/agent run, read in this order:

1. `PROJECT_RULES.md`
2. `.claude/project-memory/project-manifest.md`
3. `.claude/project-memory/current-state.md`
4. `.claude/project-memory/roadmap.json`

If any file is missing or stale, record that in the first operational response.

## Definition of Done (Operational)

A task is only operationally complete when all items below are satisfied:

- Work result is summarized in `current-state.md`.
- A checkpoint file exists for the session.
- Roadmap task status is synchronized.
- Blockers and next steps are explicit.
- Compliance status is declared.

## Task Completion Record (Required Block)

Use this block for every materially completed task:

```markdown
## Task Completion Record

- What was done: {summary}
- Files changed: {paths}
- Decisions: {key decisions and rationale}
- Blockers: {none or explicit blockers}
- Next steps: {ordered list}
- Evidence of updates:
  - current-state: {path and timestamp}
  - checkpoint: {path and timestamp}
  - roadmap status sync: {task ids and final status}
- Compliance status: {PASS | FAIL}
```

## Compliance Failure Handling

If any required artifact is missing:

- Mark `Compliance status: FAIL`.
- Explain what is missing.
- Do not close the task as operationally complete.

## Validation Scenarios

Use these checks during reviews:

1. Completed task: verify `current-state`, checkpoint, and roadmap sync are all updated.
2. New chat with no context: verify bootstrap protocol reconstructs objective, progress, and pending work.
3. Scope drift: verify guardrail warnings and correction proposal are explicit.
4. Missing checkpoint: verify output is marked `Compliance status: FAIL`.
