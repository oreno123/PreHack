# PreHack

> Pre-built hackathon wheels and skills library.
>
> 预组装黑客松开发套件与即用型工具合集。

## What This Repo Is

PreHack is not meant to be a single project.
It is a shelf of reusable components for hackathons, fast prototypes, and short-cycle builds.

PreHack 不是单一项目仓库，而是一个长期积累的组件货架。
每个组件都应该能被单独拿出来用，解决一个明确问题。

## Repository Layout

```text
PreHack/
  playbook/            # 比赛作战手册：七阶段流程 + 五类比赛 flow + 模板 + 案例
  components/          # 真正可用的独立工具、组件、微产品
  skills/              # 全局 Claude Code skills 全量备份（唯一真相源）
  docs/                # 仓库规范、组件接入规则、维护说明
  registry/            # 组件清单和索引（含 planned 候选）
  templates/           # 新组件模板
  README.md
```

## Principles

1. One component solves one clear problem.
2. Every component must have its own README.
3. Runtime state, secrets, logs, and downloads do not go into git.
4. Components should be runnable on their own.
5. The root README should stay short and act like a shelf index.

## Components

### 1. `remote-batch-studio`

- Path: [components/remote-batch-studio](./components/remote-batch-studio)
- Type: remote generation and review tool
- Status: working

What it does:

- Batch-submit prompts to remote image or video APIs
- Store task state and remote result URLs
- Review results in a local web UI with `留下 / 淘汰`
- Download only kept assets
- Export a regeneration pack for the next round

### 2. `galaxy-scene`

- Path: [components/galaxy-scene](./components/galaxy-scene)
- Type: three.js particle scene (galaxy / bronze ding / winged horse)
- Status: working

双击 start.bat 即开。32768 粒子烘焙回放 + 光管线，支持任意 mesh 经 prep/ 管线烘成粒子形态、心跳节律模式。视觉冲击类作品的现成底座。

### 3. `cn-dev-cheatsheets`

- Path: [components/cn-dev-cheatsheets](./components/cn-dev-cheatsheets)
- Type: reference cards
- Status: working

国内 Windows 环境三张速查卡：Windows 坑手册、国产 API/链上 RPC/代理速查、部署与验收配方。

### 4. `color-system-cheatsheet`

- Path: [components/color-system-cheatsheet](./components/color-system-cheatsheet)
- Type: design reference cards
- Status: working

配色与排版经验卡：等明度体系、NIO 字重经验、PPT 白底衬线基线与雷区清单。

### 5. `mathmodel-cheatsheet`

- Path: [components/mathmodel-cheatsheet](./components/mathmodel-cheatsheet)
- Type: reference cards
- Status: working

数模竞赛速查卡（CUMCM + MCM/ICM）：九大题型与出题趋势、国美赛打法差异、12 个获奖样本的可复用套路链与开源论文资源。

## Playbook

[playbook/](./playbook/README.md) 是比赛作战手册：来了一个比赛，三步开工——填画像卡 → 判型（十五型之一，复合型拼接）→ 取对应 flow。七阶段是阶段库（每张卡有输入/输出契约和退出条件），十五条 flow 分三组：交付形态（现场 48h / 线上 2-4 周 / 路演答辩 / 实物打印 / 调研报告）、专项赛型（数模 72h / 创新创业 BP / 设计征集 / 晋级制作品赛 / AI 内容创作）、赛制特色（数据竞赛 / 命题平台 / 成果报奖 / 学术论文 / 策展展示）。打完一仗回 `playbook/cases/` 补一卡复盘，教训固化回阶段卡。

## Skills

`skills/` 是全局 Claude Code skills（`~/.claude/skills/`）的全量备份，2026-11-05 起接管原 `skills-for-myself` 仓库，成为唯一备份真相源。

- 共 220 个 skill：开发工作流、GSAP 动画、营销 60+、PPT/演示、Blender、数学建模、中文自建系列等
- 快照时已剥除内嵌 `.git`（上游历史不重复存）
- 完整索引见 [skills/README.md](./skills/README.md)
- 恢复方式：把需要的目录复制回 `~/.claude/skills/`
- 新增 skill 后同步快照进来，并重新生成索引表

## How To Add A New Component

1. Copy [templates/component-template](./templates/component-template)
2. Rename it under `components/<your-component-name>`
3. Fill in the local `README.md`
4. Add component metadata to [registry/components.json](./registry/components.json)
5. Keep secrets and runtime files out of git

Detailed rules are in:

- [docs/REPO_STRUCTURE.md](./docs/REPO_STRUCTURE.md)
- [docs/ADDING_COMPONENTS.md](./docs/ADDING_COMPONENTS.md)

## Current Registry

See:

- [registry/components.json](./registry/components.json)

## Goal

The long-term goal is simple:

- stop rebuilding the same infrastructure
- keep reusable wheels in one place
- make it easy to compose a project from proven parts

长期目标也很直接：

- 少重复造轮子
- 把可复用工具集中管理
- 以后做项目时像拿积木一样组合现成组件
