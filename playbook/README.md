# PreHack Playbook — 比赛作战手册

把"比赛来了"到"提交回执"之间铺成标准工序。

## 三步开工

1. **填画像卡**（阶段 0）——把规则变成结构化信息，格式雷区前置暴露
2. **判型**——对照五型特征，确定比赛属于哪一类
3. **取对应 flow**——按 `flows/` 里那条流程文件走，它引用 `stages/` 的阶段卡并声明裁剪规则

## 阶段库（积木）

阶段卡是全量定义，flow 决定用不用、压多久。每张卡有输入契约、输出契约、退出条件。

| # | 阶段卡 | 输入 | 输出（契约） | 退出条件核心 |
|---|---|---|---|---|
| 0 | [情报](stages/0-intel.md) | 比赛公告 | 比赛画像卡 | 无空格，雷区逐条列出 |
| 1 | [选题](stages/1-ideation.md) | 画像卡+能力清单 | ≤3 候选+评分矩阵 | 唯一第一 |
| 2 | [验证](stages/2-spike.md) | 候选题 | spike 报告 | 真跑过端点，非纸面 |
| 3 | [设计](stages/3-design.md) | 选定题+spike 结论 | 90 秒演示脚本+视觉方向 | 陌生人能复述"打开后看到什么" |
| 4 | [构建](stages/4-build.md) | 设计稿 | 部署 URL+启动方式 | curl 200，手机能开 |
| 5 | [交付物](stages/5-deliverables.md) | demo+交付清单 | 逐项交付物 | 格式逐字对过 |
| 6 | [提交](stages/6-submit.md) | 交付物全家福 | 回执+自查表全绿 | 自查表全绿才提交 |

## 五条 Flow（比赛型 → 流程）

| 型 | 流程文件 | 一句话特征 |
|---|---|---|
| UC1 现场 48h | [flow-48h-onsite.md](flows/flow-48h-onsite.md) | 组件复用率=生命线 |
| UC2 线上 2-4 周 | [flow-online-2-4w.md](flows/flow-online-2-4w.md) | 全走满，验证加重 |
| UC3 路演答辩 | [flow-pitch-defense.md](flows/flow-pitch-defense.md) | 演示脚本与讲稿是主战场 |
| UC4 实物打印 | [flow-physical-print.md](flows/flow-physical-print.md) | 打印失败缓冲前置 |
| UC5 调研报告 | [flow-research-report.md](flows/flow-research-report.md) | skills 主力，数据纪律 |

## 契约原则

- **只认输入输出，不认感觉**：阶段交接看契约物是否到位
- **退出条件是硬杠杠**：没满足不许进下一阶段，宁可在本阶段砍范围
- **坑=检查点**：案例库（`cases/`）的教训固化在对应阶段卡的"坑与检查点"里，每加一条复盘就回写一张卡
- **先取轮子再造轮子**：进任何阶段先看该卡的组件清单，PreHack 的 `components/` 和 `skills/` 就是为此存在

## 模板

| 模板 | 用在 |
|---|---|
| [画像卡](templates/profile-card.md) | 阶段 0 |
| [spike 报告](templates/spike-report.md) | 阶段 2 |
| [演示脚本](templates/demo-script.md) | 阶段 3 |
| [提交自查表](templates/submit-checklist.md) | 阶段 6 |

## 案例库

见 [cases/](cases/)。每个案例一张卡：结果、核心教训、教训固化到了哪张阶段卡。打完一仗回来补一卡。
