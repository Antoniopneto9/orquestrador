# Project Manifest

## Project Name

AgentSpec

## Objective

Provide a reusable AI-native development framework that combines Spec-Driven Development with an operational project memory layer for recovery, forecasting, and scope control.

## Core Idea

Turn AgentSpec from a pure five-phase specification workflow into a hybrid system:

1. Spec-Driven Development for feature definition and delivery
2. Project operational memory for continuity, tracking, and planning

The framework should remain Claude Code compatible while also being easy to adapt procedurally in other coding-agent environments.

## Success Criteria

- New projects can initialize `.claude/project-memory/` in one step.
- Teams can recover context after a gap using `/status`.
- Weekly planning is supported by a concrete forecast artifact.
- Session checkpoints map progress to roadmap areas and tasks.
- Scope drift is visible against the original idea and guardrails.
- Existing SDD phases continue to operate without workflow regression.

## Areas of Work

| Area | Purpose | Current Target |
|------|---------|----------------|
| Framework Architecture | Preserve SDD pipeline while adding operational memory | Hybrid architecture documented |
| Commands and Agents | Add project-memory commands and operational agents | New command and agent catalog live |
| Operational Templates | Provide practical templates for future projects | Templates production-ready |
| Documentation and Adoption | Explain the hybrid workflow clearly | Main docs updated |

## Guardrails

- Preserve the existing AgentSpec philosophy and command structure.
- Prefer additive changes over breaking rewrites.
- Reuse SDD artifacts as inputs instead of duplicating them.
- Keep prompts deterministic, operational, and production-usable.
- Make the extension generic enough for all future projects initialized from this repo.

## Non-Goals

- Replacing the SDD workflow with a separate project management system
- Introducing external services or mandatory SaaS integrations
- Making project memory depend on one specific programming language
- Creating a new standalone repository

## Recommended Workflow

```text
/brainstorm -> /define -> /design -> /start-project -> /build
             -> /checkpoint -> /status -> /forecast-week -> /ship
```

Use `/checkpoint` whenever work materially changes project state. Use `/status` before resuming after a pause. Use `/forecast-week` for planning and stakeholder communication.

## Suggested Agents

| Agent | Why |
|-------|-----|
| `define-agent` | Keep project objective and success criteria aligned with requirements |
| `design-agent` | Convert DEFINE artifacts into roadmap-ready execution structure |
| `project-tracker-agent` | Keep roadmap and progress synchronized |
| `session-analyst-agent` | Turn active work into high-signal checkpoints |
| `roadmap-guardian-agent` | Detect drift against the original idea and guardrails |
| `weekly-forecaster-agent` | Produce realistic weekly planning output |
| `executive-status-agent` | Convert operational state into concise management updates |
