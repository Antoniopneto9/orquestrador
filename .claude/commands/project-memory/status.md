---
name: status
description: Recover context and summarize the current operational project state
---

# Status Command

> Build a concise recovery report from SDD artifacts plus Project Memory artifacts.

## Usage

```bash
/status
/status --feature USER_AUTH
```

## Questions This Command Must Answer

- What is the project objective?
- What has already been done?
- What remains pending?
- What changed recently?
- What is the next best action?
- Which agents should be used next?
- Is the work drifting away from the original idea?

---

## Read Order

```markdown
Read(PROJECT_RULES.md)
Read(.claude/project-memory/project-manifest.md)
Read(.claude/project-memory/roadmap.json)
Read(.claude/project-memory/current-state.md)
Read(.claude/project-memory/metrics/progress-snapshot.json)
Glob(.claude/project-memory/checkpoints/*.md)
Glob(.claude/project-memory/sessions/*.md)

Optional:
Glob(.claude/sdd/features/DEFINE_*.md)
Glob(.claude/sdd/features/DESIGN_*.md)
Glob(.claude/sdd/reports/BUILD_REPORT_*.md)
Glob(.claude/sdd/archive/**/SHIPPED_*.md)
Read(CLAUDE.md)
```

---

## Required Output

Produce a concise report with:

1. Project objective
2. Overall progress percentage
3. Progress by area
4. Recently completed work
5. Pending work
6. Decisions already taken
7. Next recommended step
8. Recommended commands
9. Recommended agents
10. Scope drift risk
11. Compliance status: PASS/FAIL

---

## Synthesis Rules

- Prefer project-memory artifacts for live state
- Use SDD artifacts to validate and enrich live state
- If roadmap and recent checkpoints disagree, call out the mismatch
- If no checkpoint exists, infer status from latest DEFINE, DESIGN, and BUILD artifacts
- Guardrail warnings must be explicit, not buried

---

## Quality Gate

```text
[ ] Objective is stated in one sentence
[ ] Progress is quantified
[ ] Pending work is concrete
[ ] Recommended next step is singular and actionable
[ ] Agent recommendations fit the current phase
[ ] Drift risk is assessed
[ ] Compliance status is explicitly declared
```

---

## Compliance Gate

Before closing `/status`:

```text
[ ] Bootstrap protocol was respected
[ ] State, checkpoints, and roadmap were checked together
[ ] Any missing documentation is called out explicitly
[ ] Output includes "Compliance status: PASS/FAIL"
```

---

## References

- Rules: `PROJECT_RULES.md`
- Template: `.claude/project-memory/templates/status-template.md`
- Related commands: `.claude/commands/project-memory/checkpoint.md`, `.claude/commands/project-memory/forecast-week.md`
