# Core Concepts

Understanding the mental model behind AgentSpec's hybrid workflow.

## The Problem

AI-assisted development fails in two ways when structure is missing:

- Requirements and design decisions are lost
- Day-to-day execution context is lost

Spec-Driven Development solves the first problem. Project Memory solves the second.

## The Two-Layer Model

```text
Specification Layer
/brainstorm -> /define -> /design -> /build -> /ship

Operational Layer
             /start-project -> /checkpoint -> /status -> /forecast-week
```

The layers are complementary, not competing.

## Layer 1: Spec-Driven Development

SDD captures:

- the problem
- the target users
- the success criteria
- the architecture
- the implementation plan
- the shipped lessons learned

## Layer 2: Project Memory

Project Memory captures:

- the original project objective
- roadmap areas and task progress
- session checkpoints
- decisions and blockers over time
- recovery-ready current state
- weekly forecast and executive summaries
- scope drift against original guardrails

## Why Both Matter

A good spec tells you what should happen. A good operational memory system tells you what actually happened and what should happen next.

## Recommended Use

- Use `/start-project` once the project has enough definition to initialize its operational structure.
- Use `/checkpoint` whenever a session changes project state.
- Use `/status` before resuming work after a gap.
- Use `/forecast-week` to keep planning realistic.
- Use `roadmap-guardian-agent` when new requests may distort scope.
