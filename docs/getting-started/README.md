# Getting Started with AgentSpec

Get from zero to a working hybrid delivery flow in 10 minutes.

## Prerequisites

- Claude Code CLI installed
- Git

If you are using another coding agent, treat the command files in `.claude/commands/` as procedural runbooks and keep the same artifact flow.

Read `PROJECT_RULES.md` before any operational execution. It is the normative source for documentation compliance.

## Installation

Clone the AgentSpec framework into your project:

```bash
git clone https://github.com/luanmorenommaciel/agentspec.git
cp -r agentspec/.claude your-project/.claude
```

## Initialize Your Project

The hybrid directory structure is already set up:

```text
your-project/.claude/
|-- agents/            # Workflow, operational, quality, communication, exploration agents
|-- commands/          # Workflow, project-memory, core, knowledge, review commands
|-- sdd/               # Spec-Driven Development artifacts
|-- project-memory/    # Roadmap, checkpoints, metrics, status, reports
`-- kb/                # Domain knowledge
```

## Recommended Flow

### Step 1: Brainstorm

```bash
claude> /brainstorm "I want to add user authentication with JWT"
```

### Step 2: Define

```bash
claude> /define USER_AUTH
```

### Step 3: Design

```bash
claude> /design USER_AUTH
```

### Step 4: Start the Project Memory Layer

```bash
claude> /start-project "User Authentication"
```

This creates `project-manifest.md`, `roadmap.json`, `current-state.md`, and initial metrics.

### Step 5: Build

```bash
claude> /build USER_AUTH
```

### Step 6: Save Checkpoints During Execution

```bash
claude> /checkpoint
```

### Step 7: Recover Context When Resuming

```bash
claude> /status
```

### Step 8: Plan the Next Week

```bash
claude> /forecast-week
```

### Step 9: Ship

```bash
claude> /ship USER_AUTH
```

## What the New Layer Adds

- `project-manifest.md` keeps the original idea, objective, guardrails, and recommended workflow.
- `roadmap.json` tracks areas, tasks, dependencies, and progress.
- `current-state.md` gives a recovery-ready snapshot.
- `checkpoints/` stores timestamped operational snapshots.
- `metrics/` and `reports/` support planning and executive communication.

## Operational Definition of Done

A materially completed task is only done when:

- `current-state.md` was updated
- a checkpoint file was created
- applicable roadmap task statuses moved to `done`
- the close-out includes `Compliance status: PASS/FAIL`

Use the required `Task Completion Record` from `PROJECT_RULES.md` to close every task consistently.
