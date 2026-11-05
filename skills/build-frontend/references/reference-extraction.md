---
name: reference-extraction
description: 从图片/URL/设计稿中提取设计要素的模式 — 支持本地截图、网页 URL、设计稿、混合参考
---

# Reference Extraction Pattern

## 模式说明

用户说「做成这个样子」并给出参考素材。Claude 从中提取可操作的设计 tokens（配色、字体、布局、组件），作为生成的硬约束。

## 输入类型与处理策略

### Type A: 本地截图/图片

**触发**：用户给出文件路径（如 `D:/screenshots/ref.png`）

**Claude 操作**：
1. 使用 Read 工具读取图片（Claude 支持图片理解）
2. 提取以下要素并输出为结构化格式

**提取清单**：

```
1. 配色方案
   - 主色（出现面积最大的颜色）
   - 辅色（第二大面积）
   - 强调色（小面积、高对比）
   - 背景色
   - 文字色
   → 全部转为 HEX 值

2. 字体风格
   - 标题字体：[衬线 | 无衬线 | 手写 | 装饰] + [粗重 | 轻盈 | 常规]
   - 正文字体：[衬线 | 无衬线 | 等宽] + [大 | 中 | 小] 字号感觉
   → 映射为具体 Google Fonts 推荐（如"衬线粗重"→ Playfair Display 900）

3. 布局模式
   - [单栏居中 | 双栏 | 三栏 | 网格 | 层叠 | 全屏分区]
   - 头部区域特征
   - 内容区域特征
   - 底部区域特征

4. 组件清单
   - 列出可见的 UI 组件（导航栏、卡片、按钮、列表、表单等）
   - 每个组件的关键样式特征

5. 动效暗示
   - 如果截图暗示了动画（如渐变背景、浮动元素、视差层）
   - 标注可能的动效类型

6. 整体调性
   - 3-5 个关键词（如：暗黑奢华、温暖文艺、赛博朋克、极简主义）
```

### Type B: 网页 URL

**触发**：用户给出网址（如 `https://stripe.com`）

**Claude 操作**：
1. 使用 WebFetch 或 mcp__web-reader__webReader 工具抓取页面
2. 优先提取 `<style>` 标签和内联样式中的 CSS 变量
3. 提取 Google Fonts URL 中的字体名
4. 分析 HTML 结构（semantic elements、grid/flex layout）

**提取重点**（视觉层 > 代码层）：

```
1. CSS 变量 / 设计 tokens
   - 搜索 :root 或 html 选择器中的变量定义
   - 提取颜色、字号、间距变量

2. 字体
   - 从 Google Fonts <link> 中提取 font-family
   - 从 font-family CSS 属性中提取

3. 配色
   - background-color 出现频率最高的值
   - color 属性的常用值
   - border-color / accent-color

4. 布局结构
   - grid-template-columns / rows
   - flex 方向和间距
   - section 的数量和顺序

5. 交互特征
   - hover 效果描述
   - transition / animation 属性
   - 滚动相关（position:sticky、IntersectionObserver）
```

### Type C: 设计稿文件

**触发**：用户提供 Figma 导出图、Sketch 截图等

**处理**：等同于 Type A（当作图片处理），额外关注：
- 标注的间距数值（如有）
- 颜色标注
- 组件状态（normal/hover/active）

### Type D: 混合参考

**触发**：用户同时给图片 + URL + 文字描述

**处理策略**：
1. 分别提取每个输入的设计 tokens
2. 以「图片」为最高优先级（视觉最具体）
3. URL 次之（提供结构信息）
4. 文字描述补充语义（用途、调性）
5. 冲突时：图片 > URL > 文字

## 输出格式

所有类型统一输出为「参考摘要表」：

```
## 参考摘要

**配色方案**
- 主色：#1a1a2e
- 辅色：#16213e
- 强调色：#e94560
- 背景：#0f3460
- 文字：#ffffff / #a8a8b3（次级）

**字体方向**
- 标题：衬线粗体 → 推荐 Playfair Display 900 或 Cormorant Garamond 700
- 正文：无衬线轻盈 → 推荐 DM Sans 400 或 Outfit 300
- 强调/装饰：等宽 → 推荐 JetBrains Mono 500

**布局**
- 全屏分区滚动，每屏一个主题
- 顶部固定导航（半透明毛玻璃）
- 内容区居中，max-width: 1080px

**组件**
- 导航栏、Hero 全屏区、特性三列卡片、CTA 区、Footer
- 按钮：圆角大按钮，hover 时有阴影扩散

**动效**
- 滚动驱动的 fade-in-up
- 导航栏滚动后变实色
- 卡片 hover 上浮 + 阴影

**调性关键词**
- 暗黑科技、深邃神秘、专业精致、微妙的赛博感
```

输出后**必须**询问用户确认：「我从参考中理解到这些，对吗？需要调整什么？」

## 图片 Base64 嵌入

当用户提供图片要求内嵌到生成页面时：

```
1. 读取图片文件
2. 转为 base64 data URL：data:image/png;base64,{data}
3. 在生成的 HTML 中作为 <img src="data:image/png;base64,..."> 嵌入
4. 禁止用 Unsplash/picsum 替代用户的真实图片
```

注意：单张图片 base64 超过 500KB 时应提醒用户可能影响加载性能。

## 适用场景

- 「做成这个网站的样子」
- 「参考这个设计稿」
- 「我喜欢这个截图的配色」
- 任何需要将视觉参考转化为可操作设计约束的场景
