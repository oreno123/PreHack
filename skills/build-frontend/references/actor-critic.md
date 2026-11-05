---
name: actor-critic
description: 生成器+评论家循环模式 — 独立评分 → gap 反馈 → 再生成，适用于任何 AI 生成+质量保证场景
---

# Actor-Critic Loop Pattern

## 模式说明

将「生成」和「评估」分离为两个独立角色，形成闭环反馈：

```
用户需求 → [Actor 生成] → 成品 v1 → [Critic 评分] → 分数 + gaps
                                                          ↓
                                            分数 < 3.5 且迭代 < max?
                                                 ↓ Yes
                                    gaps 喂回 Actor → 成品 v2 → [Critic] → ...
```

## 核心原则

1. **角色隔离**：Actor 和 Critic 不能是同一个上下文。Critic 必须以全新视角看成品，不知道生成过程中的任何决策。
2. **保守评分**：Critic 应默认 Actor 会虚报质量。打分时减去 0.4~0.75 的"生成者乐观偏差"。
3. **结构化反馈**：Critic 输出不是自然语言评论，而是 JSON `{ score, gaps[], ship, veto_hit }`。
4. **有限迭代**：最多 2 轮（共 3 次生成机会）。超过则强制交付当前最好版本。
5. **Gap 具体**：每条 gap 必须引用具体的评分项 ID（如 "R-05 背景为纯色"），不能是模糊抱怨。

## Claude Code 中的实现

在 Claude Code 环境中，Actor 就是 Claude 本身，Critic 通过 `Agent` 工具启动独立 sub-agent 实现。

### Actor 阶段（Claude 主对话）

1. 接收用户需求 + 参考素材 + 维度
2. 生成完整 HTML 文件
3. 自检一票否决项（如有命中，立即修复）
4. 写入文件
5. 启动 Critic sub-agent

### Critic 阶段（sub-agent）

Critic 的 system prompt：

```
You are the critic — independent of the generator.
Score the HTML against the quality rubric.
Be conservative: assume the generator inflated 0.4 ~ 0.75.
Return ONLY JSON, no commentary, no markdown fences:
{"score": <number 0-5>, "gaps": ["ID 具体问题", ...], "ship": <boolean>, "veto_hit": <string|null>}
```

Critic 收到的用户消息：

```
评分以下 HTML：

[截取前 10000 字符的 HTML 内容]

Return ONLY the JSON.
```

### 迭代决策（回到 Actor）

```
if ship=false and score < 3.5 and iteration < 2:
    prev_gaps = critic.gaps
    iteration += 1
    重新生成，在 prompt 中附带：
    "这是你第 {iteration} 轮。上一轮 critic 打了 {score}/5，找到这些差距：
     {gaps}
    请针对这些 gap 重新写一版。"
    generate_again(prev_gaps)
else:
    deliver()
```

### 关键代码模式（源自 ip-website-studio builder.js）

**迭代状态管理**：
```javascript
let iteration = 0;
let prevCriticFeedback = null;
const MAX_ITERATIONS = 2;
```

**Critic 结果解析**：
```javascript
const jsonMatch = text.match(/\{[\s\S]*\}/);
const parsed = JSON.parse(jsonMatch[0]);
lastCritic = {
  score: typeof parsed.score === 'number' ? parsed.score : 0,
  gaps: Array.isArray(parsed.gaps) ? parsed.gaps : [],
  ship: !!parsed.ship,
};
```

**迭代决策**：
```javascript
if (lastCritic.ship === false &&
    (lastCritic.score ?? 5) < 3.5 &&
    iteration < MAX_ITERATIONS) {
  prevCriticFeedback = lastCritic;
  iteration += 1;
  await runOneIteration(); // 递归
}
```

## 适用场景

- 前端页面生成（本 skill）
- 代码生成 + 质量审查
- 文档撰写 + 可读性评分
- 任何「生成→评估→改进」循环

## 自适应变体

根据场景复杂度调整参数：

| 场景 | MAX_ITERATIONS | ship 阈值 | 评分维度数 |
|------|---------------|-----------|-----------|
| 简单海报 | 1 | 3.0 | 10 项 |
| 完整网页 | 2 | 3.5 | 20 项 |
| 复杂应用 | 3 | 4.0 | 30+ 项 |
