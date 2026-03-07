# AgentSpec Development

Developing the hybrid Spec-Driven Development plus Project Memory framework.

---

## Project Context

**What is AgentSpec?** A Claude Code framework that combines structured feature delivery with operational project memory.

**Current Status:** Framework ready with Project Memory extension integrated.

## Mandatory Session Bootstrap

Every new session MUST start by reading:

1. `PROJECT_RULES.md`
2. `.claude/project-memory/project-manifest.md`
3. `.claude/project-memory/current-state.md`
4. `.claude/project-memory/roadmap.json`

If any of these artifacts are missing or outdated, report it before operational execution.

---

## Repository Structure

```text
agentspec/
|-- .claude/
|   |-- agents/
|   |   |-- workflow/
|   |   |-- operations/
|   |   |-- code-quality/
|   |   |-- communication/
|   |   `-- exploration/
|   |-- commands/
|   |   |-- workflow/
|   |   |-- project-memory/
|   |   |-- core/
|   |   |-- knowledge/
|   |   `-- review/
|   |-- sdd/
|   |-- project-memory/
|   `-- kb/
|-- docs/
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- SECURITY.md
`-- README.md
```

## Recommended Development Flow

```bash
/brainstorm "Add a new framework capability"
/define FEATURE_NAME
/design FEATURE_NAME
/start-project "Feature Name"
/build FEATURE_NAME
/checkpoint
/status
/forecast-week
/ship FEATURE_NAME
```

## Commands Available

- `/brainstorm`
- `/define`
- `/design`
- `/start-project`
- `/build`
- `/checkpoint`
- `/status`
- `/forecast-week`
- `/ship`
- `/iterate`
- `/create-pr`
- `/create-kb`
- `/review`
- `/memory`
- `/sync-context`
- `/readme-maker`

## Operational Rules

- Follow rule precedence: `PROJECT_RULES.md` > `.claude/project-memory/README.md` > command files.
- Align project manifest content with DEFINE when available.
- Derive roadmap tasks from DESIGN when available.
- Use BUILD reports and checkpoints to keep current state current.
- For materially completed tasks, update `current-state.md`, create checkpoint, and sync roadmap task status.
- Every relevant operational close-out MUST include `Compliance status: PASS/FAIL`.
