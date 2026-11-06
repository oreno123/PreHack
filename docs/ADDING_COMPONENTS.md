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

### 契约字段（必填）

组件必须声明与 playbook 阶段的契约，六项不填全不算入架：

```json
{
  "stages": [2],
  "input": "它吃什么：文件/URL/配置的形态与格式",
  "output": "它吐什么：交付物形态与落盘位置",
  "use_when": "什么场景下取这个轮子",
  "not_for": "什么场景别用它",
  "integration_time": "~2h"
}
```

- `stages`：服务于 [playbook](../playbook/README.md) 的哪些阶段（0-6，见阶段库）
- 其余四项写人话，写得让凌晨三点的自己能看懂

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
