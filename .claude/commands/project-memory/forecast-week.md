---
name: forecast-week
description: Estimate realistic progress for the next week from roadmap and execution history
---

# Forecast Week Command

> Produce a realistic weekly forecast grounded in recent checkpoints, remaining roadmap, and current delivery signals.

## Usage

```bash
/forecast-week
/forecast-week --week-of 2026-03-09
```

## What It Does

1. Analyzes recent checkpoints and sessions
2. Reads roadmap remaining work and progress by area
3. Reviews unfinished work and blockers
4. Generates:
   - probable completions next week
   - likely blockers
   - suggested focus areas
   - recommended agent sequence
   - confidence and realism notes
5. Writes:
   - `.claude/project-memory/reports/executive-status.md`
   - `.claude/project-memory/metrics/weekly-metrics.json`

---

## Read Order

```markdown
Read(PROJECT_RULES.md)
Read(.claude/project-memory/roadmap.json)
Read(.claude/project-memory/current-state.md)
Read(.claude/project-memory/metrics/progress-snapshot.json)
Glob(.claude/project-memory/checkpoints/*.md)
Glob(.claude/project-memory/sessions/*.md)

Optional:
Glob(.claude/sdd/reports/BUILD_REPORT_*.md)
Glob(.claude/sdd/features/DESIGN_*.md)
Glob(.claude/sdd/archive/**/SHIPPED_*.md)
```

---

## Forecast Logic

### Completion Candidates

Prefer tasks that are:

- already in progress
- low dependency
- recently active
- backed by recent BUILD evidence

### Risk Signals

Raise risk when:

- blockers repeat across checkpoints
- too many areas are active at once
- roadmap tasks remain vague
- progress changed little in the current week
- execution is drifting beyond guardrails

### Focus Rule

Recommend one primary focus area for the week unless the roadmap clearly requires parallel streams.

---

## Output Expectations

The report must include:

- likely completions
- progress delta estimate
- risk areas
- focus recommendation
- recommended agent sequence
- confidence and realism notes
- compliance status: PASS/FAIL

---

## Quality Gate

```text
[ ] Forecast is grounded in recent evidence
[ ] Planned completions are realistic
[ ] Risks are explicit
[ ] Focus area is singular or clearly justified
[ ] Agent sequence matches the likely work
[ ] Metrics file is updated consistently with report
[ ] Compliance status is explicitly declared
```

---

## Compliance Gate

Before closing `/forecast-week`:

```text
[ ] Forecast used current-state + roadmap + checkpoints
[ ] Missing checkpoint/state evidence is reported
[ ] Output includes "Compliance status: PASS/FAIL"
```

---

## References

- Rules: `PROJECT_RULES.md`
- Template: `.claude/project-memory/templates/forecast-template.md`
- Report output: `.claude/project-memory/reports/executive-status.md`
- Metrics output: `.claude/project-memory/metrics/weekly-metrics.json`
