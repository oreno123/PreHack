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
