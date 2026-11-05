---
name: quality-rubric
description: 评分量表模板 — 用于 Actor-Critic 循环中 critic sub-agent 对生成 HTML 的质量评估
---

# Quality Rubric

## 评分规则

- 分数范围：0 ~ 5，步进 0.05
- ship 判定：score ≥ 3.5 且无一票否决项违反
- critic 默认假设生成器虚报 0.4 ~ 0.75 分，应保守评分

## 一票否决项（VETO — 任一命中即 ship=false）

| ID | 项目 | 检查方式 |
|----|------|----------|
| V-01 | Broken image | `<img>` 的 src 为空、指向不存在的路径、或指向 unsplash/picsum/placeholder.com |
| V-02 | 死交互 | `<a href="#">`、空 `<button>` 无 onclick、表单无 action 且无 JS 处理 |
| V-03 | 占位文案 | Lorem ipsum、`TODO`、`FIXME`、`Your text here`、`Insert X here` |
| V-04 | 未定义 CSS 变量 | `var(--xxx)` 使用了但未在 `:root` 或任何选择器中定义 |
| V-05 | AI slop 命中 | 字体三件套（Inter + 紫色渐变 + Space Grotesk）同时出现 |
| V-06 | alert/prompt/confirm | 使用了浏览器原生弹窗 |

## 评分维度

### 视觉（权重 30%）

| ID | 项目 | 满分标准 |
|----|------|----------|
| R-01 | 配色一致性 | 所有颜色来自统一的调色板，无不协调的随机色 |
| R-02 | 字体配对 | 标题+正文+强调最多 3 种字体，配对和谐且有对比 |
| R-03 | 留白与密度 | 间距有节奏感，不拥挤不空旷，关键元素有呼吸空间 |
| R-04 | 视觉层次 | 大小、粗细、颜色形成清晰的信息层次（h1→h2→p→small） |
| R-05 | 背景氛围 | 非纯色平面 — 有纹理、渐变、噪点、图案或分层叠加 |

### 排版（权重 15%）

| ID | 项目 | 满分标准 |
|----|------|----------|
| R-06 | 行长与行高 | 正文行宽 45-75 字符，行高 1.5-1.8 |
| R-07 | 标题排版 | 标题有 letter-spacing 调整，无孤字（orphan） |
| R-08 | 响应式文字 | 移动端可读，clamp() 或 media query 适配 |

### 动效（权重 15%）

| ID | 项目 | 满分标准 |
|----|------|----------|
| R-09 | 入场动画 | 页面加载有 staggered reveal 或淡入，非瞬间全部出现 |
| R-10 | 交互反馈 | hover/focus/active 有明确的视觉变化 |
| R-11 | 动效节制 | 无 gratuitous 旋转/弹跳/闪烁，每帧都有目的 |

### 可用性（权重 20%）

| ID | 项目 | 满分标准 |
|----|------|----------|
| R-12 | 移动端适配 | 移动端布局合理，无水平溢出，触控目标 ≥ 44px |
| R-13 | 可读性 | 文字与背景对比度 ≥ 4.5:1（正文），≥ 3:1（大标题） |
| R-14 | 导航可用 | 如有导航，每个链接指向有效目标（页内锚点或实际 URL） |
| R-15 | 加载体验 | 字体显示不闪烁（font-display:swap 或 preconnect） |

### 代码质量（权重 20%）

| ID | 项目 | 满分标准 |
|----|------|----------|
| R-16 | CSS 变量系统 | 设计 tokens（颜色、字号、间距）用 CSS 变量统一管理 |
| R-17 | 语义 HTML | 使用 header/main/section/article/footer/nav 而非全 div |
| R-18 | 无冗余代码 | 无注释掉的代码、无空 CSS 规则、无未引用的 class |
| R-19 | 框架使用正确 | Vue/React 代码遵循框架最佳实践，无反模式（如直接 DOM 操作） |
| R-20 | 性能意识 | 图片有尺寸标注、无超大 base64（>500KB 图片应考虑压缩） |

## Critic 输出格式

```json
{
  "score": 4.15,
  "gaps": ["R-05 背景为纯色，缺少氛围层", "R-09 无入场动画"],
  "ship": true,
  "veto_hit": null
}
```

如果一票否决项命中：
```json
{
  "score": 2.80,
  "gaps": ["V-01 发现 2 张 broken image", "R-03 间距不均匀"],
  "ship": false,
  "veto_hit": "V-01"
}
```

## Refinement 原则

借鉴 `canvas-design` 的 refinement pass 概念：
- 回去打磨现有的，而不是添加更多内容
- 如果分数差一点就到 3.5，优先修复 gaps 而非重写
- 每次迭代应让至少 2 个 gap 得到改善
