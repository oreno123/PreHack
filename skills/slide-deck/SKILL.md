---
name: slide-deck
description: "Claude Code 幻灯片生成器 — 基于 34 套精美 HTML 模板，按调性匹配选模板、替换内容、交付可双击打开的 HTML deck。触发词：做个 PPT、做幻灯片、slide deck、presentation、做个演示、做个演讲稿、做 deck。"
---

# slide-deck

Claude Code 幻灯片生成器。基于 [beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) 的 34 套精心设计模板，按调性匹配选模板，替换内容，交付可双击打开的 HTML deck。

**模板库路径**：`C:\Users\lenovo\.claude\skills\slide-deck\templates\`
**模板数量**：34 套（含 index.json 元数据 + design.md 设计系统文档 + template.html）
**核心特性**：调性匹配选模板、标题页预览对比、内容替换、设计系统扩展

## 主流程

```
Step 1 · 问场合+调性  →  两个关键问题
Step 2 · 读 index.json →  匹配 3 个候选模板
Step 3 · 预览标题页    →  生成 3 个单页 HTML 供对比
Step 4 · 用户选定      →  确认选择
Step 5 · 适配完整 deck  →  替换内容，扩展/裁剪 slide
Step 6 · 交付          →  写入文件，浏览器打开
```

---

## Step 1 · 问场合 + 调性

问两个问题（不要跳过）：

1. **场合是什么？**（创始人路演、季度回顾、学术报告、品牌发布、课程开场...）
2. **想要什么调性/氛围？**（自信犀利、安静文艺、温暖活泼、暗黑奢华...）

即使用户的描述已经很明显，也要问 — 用户的品味往往比推断的意图更出人意料。

---

## Step 2 · 读 index.json，匹配 3 个候选

读取 `C:\Users\lenovo\.claude\skills\slide-deck\templates\index.json`。

匹配逻辑：
- **主要依据**：`mood` + `tone` + `best_for` — 匹配用户想要的*感觉*
- **辅助判断**：`formality` 和 `density` — 检验是否匹配用户受众
- **不要过度拟合 `occasion`** — 那是举例，不是限定列表
- **`avoid_for` 是软警告，不是否决** — 如果用户明确要求某种风格，用户优先

**三个候选应该彼此不同** — 不要选三个编辑系模板；选一个编辑系、一个更温暖的替代、一个重新诠释的意外之选。

---

## Step 3 · 预览标题页

对每个候选模板：

1. 读取模板的 `template.html`
2. 取**第一张 slide**（封面/标题页）
3. 用用户的**实际标题/副标题/作者/日期**替换占位内容
4. 保存为独立 HTML（保留所有必要的 sibling assets）

告知用户三个选项，附文件路径：
```
三个选项：
1. **Studio** — 黑底电黄，设计工作室高能量
   `/path/to/preview-1.html`
2. **Soft Editorial** — 暖纸衬线，文艺安静
   `/path/to/preview-2.html`
3. **Neo-Grid Bold** — 霓虹黄新粗野，自信编辑风
   `/path/to/preview-3.html`

选哪个？
```

---

## Step 4 · 用户选定

等用户选择。不替用户决定。

---

## Step 5 · 适配完整 deck

选定后，克隆模板文件夹到用户工作目录，然后适配：

### 必须保留（这是设计系统）

- **字体** — 模板从 Google Fonts 导入的字体，不可替换
- **配色** — 所有 `:root` CSS 变量和颜色值，不可改色
- **布局网格** — grid columns、absolute positioning、flex 层级，不可重构
- **Slide 级 CSS 类**（如 `.s-toc`、`.slide--quote`、`.layout-cover`）
- **装饰元素** — 角括号、纸张纹理、几何形状、SVG 装饰，它们是视觉系统的一部分
- **导航运行时** — `deck-stage.js`、inline keyboard handler、scroll-snap 等

### 必须替换（这是用户内容）

- **标题** — `<h1>`、`<h2>`、`<h3>` 等
- **正文** — `<p>`、列表项、说明文字
- **数字和统计** — 占位值如 `47%`、`2.4M`、`+142%`
- **名字、日期、署名** — 作者名、引用行、日期占位
- **图片占位** — 替换 `<div class="img-placeholder">` 为用户的真实图片

### 增减 Slide

- 需要更多 slide → 复制最合适布局的现有 slide，替换内容
- 需要更少 slide → 从底部删除

### 设计缺失布局

如果用户需要模板没有的 slide 布局（如对比表、时间线）：
- **用模板的设计系统从零设计**，不要放弃，不要换模板
- 同样的字体、配色、装饰词汇、间距节奏、组件语法
- 新 slide 应该看起来像模板的自然延伸，不是嫁接

### 写入 DESIGN.md（托管区块）

适配完成后，在克隆的 deck 文件夹里写 `DESIGN.md`：

- `<!-- DESIGN_MANAGED_START -->` 与 `<!-- DESIGN_MANAGED_END -->` 之间放机器生成区：模板名、从 `:root` 提取的配色 CSS 变量、字体清单、布局/装饰词汇、从零设计过的 slide 清单（编号 + 布局说明）
- 标记之外留给用户手写备注

**后续修改时**：先读这份 DESIGN.md——托管区块是设计系统快照，新增/重做 slide 必须遵守；标记外的用户要求优先。只有设计 tokens 真的变化时才重写托管区块，且**只替换标记之间的内容**，标记外一个字不动。

---

## Step 6 · 交付

- 写入文件到用户指定位置
- 在浏览器中打开（`open` 或 `start` 命令）
- 告知文件路径
- 一句话说明选了哪个模板及原因
- 如有注意事项（如"我根据设计系统从零设计了第 4 和第 7 张 slide"），一并说明

---

## 调性优先匹配原则

模板有**调性**，没有行业。`best_for` 描述的是*感觉*，不是行业归属：
- 一个自信编辑风的 deck 可以承载技术演讲
- 一个活泼柔和的 deck 可以承载财务复盘
- **用户的品味优先**

---

## 触发词

做个 PPT、做幻灯片、slide deck、presentation、做个演示、做个演讲稿、做 deck、HTML PPT、网页幻灯片

## 注意事项

- 不要跳过 Step 1（问场合+调性）
- 不要跳过 Step 3（预览标题页让用户选）
- 不要替换字体（"Inter 差不多" — 不，字体就是设计系统）
- 不要改色（即使小改动也会破坏配色和谐）
- 不要混合不同模板的布局（每个模板是封闭的视觉系统）
- 不要去掉"多余的"装饰（角括号、纸张纹理都是视觉身份的一部分）
- 不要试图"现代化"旧模板（它们按设计工作，如果觉得过时，选不同的模板）
- 不要整文件覆盖 `DESIGN.md`，只更新 `DESIGN_MANAGED` 标记之间的内容；没有标记的旧文件视为用户文件，不覆盖
