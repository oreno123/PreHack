# Repo Structure

## Purpose

This repository is a component shelf.
It is designed to hold multiple reusable tools rather than one monolithic codebase.

## Top-Level Rules

### `components/`

Put all real, runnable tools here.

Each component should:

- have a clear single purpose
- contain its own README
- be runnable without depending on sibling components
- keep its runtime state and secrets ignored

### `playbook/`

The competition playbook: how a hackathon runs end to end.

- `README.md` — entry point: profile card → match a flow → follow stage cards
- `stages/0-6.md` — stage library; each card has input contract, output contract, task list, exit criteria, pitfalls, tools
- `flows/` — five competition-type flows (48h onsite / online 2-4w / pitch defense / physical print / research report); a flow composes stages with trim/boost rules
- `templates/` — profile card, spike report, demo script, submit checklist
- `cases/` — post-mortem cards: result, lesson, which stage card the lesson was baked into

Rules:

- stages are the full definitions; flows only compose and trim them — flow files must not redefine a stage
- every post-mortem lesson must be baked back into a stage card's "pitfalls" section, not left only in the case file
- a case card with unfilled "待补" items is acceptable; a fabricated detail is not

### `skills/`

Full snapshot backup of global Claude Code skills (`~/.claude/skills/`).

Rules:

- each subdirectory is one skill, exactly as it loads in Claude Code
- nested `.git` directories are stripped when snapshotting (upstream history is not duplicated here)
- `skills/README.md` is the generated index table; regenerate it after adding or removing skills
- runtime junk (eval outputs, caches) should not be committed

### `docs/`

Put repo-level conventions here.

Examples:

- structure rules
- contribution rules
- naming conventions
- maintenance guidance

### `registry/`

Put machine-readable indexes here.

This is where the repo can later grow into:

- a searchable catalog
- a launcher
- an internal docs site

### `templates/`

Put starter templates here for new components.

## Naming

- directories: kebab-case
- component ids: kebab-case
- file names: prefer lowercase and predictable names

## What Should Not Be Committed

- local runtime state
- API keys
- provider secrets
- downloaded result assets
- temp logs
- large generated files unless they are required examples

## Ideal Component Shape

```text
components/<component-name>/
  README.md
  component.json
  .gitignore
  src-or-runtime-files
```

## Scaling Direction

As the repo grows, components can later be grouped by category, but early on we keep them flat under `components/` so discovery stays easy.
