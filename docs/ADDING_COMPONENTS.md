# Adding Components

## Minimum Checklist

Every new component should include:

1. `README.md`
2. `component.json`
3. `.gitignore`
4. a runnable entrypoint or clear usage command
5. a short registry entry in `registry/components.json`

## README Expectations

Each component README should answer:

- what problem it solves
- how to start it
- what config it needs
- what files are safe to edit
- what files are generated at runtime

## `component.json` Expectations

Suggested fields:

```json
{
  "id": "component-id",
  "name": "Human Name",
  "category": "tool",
  "status": "working",
  "entry": "server.mjs",
  "readme": "README.md",
  "tags": ["tag-a", "tag-b"]
}
```

## Registry Expectations

Add one object to `registry/components.json` for every component.

The registry is intentionally simple for now so it can later feed:

- a docs site
- a launcher page
- search
- tagging

## Good Boundaries

A good component:

- solves one concrete workflow
- has small, understandable configuration
- does not assume the whole repo must run together

## Bad Boundaries

Avoid components that:

- mix several unrelated workflows
- rely on manual tribal knowledge to start
- commit local secrets or mutable runtime output
