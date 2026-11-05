---
name: build-frontend
description: "Claude Code 前端页面生成器 — 描述需求 + 参考素材，生成单文件 HTML（支持 Vue/React CDN），Actor-Critic 自评迭代，产出可直接打开的成品。触发词：做个网页、生成页面、建个站、landing page、single file HTML、portfolio page、海报页、宣传页、build a page、make a website。"
---

# build-frontend

Claude Code 前端页面生成器。用户描述需求（可附带参考图/URL），Claude 生成单文件 HTML，自动走 Actor-Critic 自评迭代，交付可双击打开的成品。

**支持技术栈**：原生 HTML/CSS/JS、Vue 3 CDN、React CDN、Three.js
**核心特性**：Actor-Critic 自评循环、参考图/URL 动态提取、零 build 步骤

## 主流程

```
Step 1 · 需求挖掘    →  问清 5 个维度
Step 2 · 参考收集    →  从图片/URL/设计稿提取设计 tokens
Step 3 · 选技术栈+维度 →  原生/Vue/React + 6 维度匹配
Step 4 · 生成（Actor） →  写出完整 HTML
Step 5 · Actor-Critic  →  自检 + 独立 sub-agent 评分 + 迭代
Step 6 · 交付        →  写入 output/ 文件
```

---

## Step 1 · 需求挖掘

一次问完 5 个维度（不要逐个追问）。如果用户描述已覆盖，直接总结确认。

| 维度 | 问题 | 示例 |
|------|------|------|
| 用途 | 这个页面做什么用？ | 作品集、产品落地页、活动海报、表白页 |
| 动效 | 要什么程度的动效？ | 纯静态、subtle hover、滚动驱动、全屏动画 |
| 媒体 | 需要嵌入什么？ | 无、BGM、视频背景、图片画廊 |
| 时长 | 单屏海报还是长滚动？ | 一屏、3-5 屏、无限滚 |
| 调性 | 整体感觉？ | 极简、暗黑奢华、温暖文艺、赛博朋克 |

### taste JSON 解析（来自 design-studio 流水线）

当用户粘贴了 taste-picker 的输出 JSON 时，从中提取所有参数，跳过对应维度的询问。JSON 结构如下：

```json
{
  "taste": {
    "dials": { "designVariance": 7, "motionIntensity": 6, "visualDensity": 4 },
    "rules": { "typography": {...}, "color": {...}, "layout": {...}, "aiTells": {...}, ... }
  },
  "source": {
    "colors": { "mode": "light", "colors": [{"name":"blue","step":9,"hex":"#0090ff"}] },
    "style": { "category": "web", "styleId": "apple", "styleName": "Apple", "tags": [...] }
  }
}
```

**提取规则：**

| JSON 路径 | 覆盖的维度 | 行为 |
|-----------|-----------|------|
| `taste.dials.motionIntensity` | 动效 | 不再询问动效等级，按 Step 3 的「动效等级映射」表生成 |
| `taste.dials.designVariance` | 布局 | 不再询问布局偏好，按 Step 3 的「布局方差映射」表生成 |
| `taste.dials.visualDensity` | 间距 | 不再询问信息密度，按 Step 3 的「视觉密度映射」表生成 |
| `taste.rules.typography.*` | 字体 | 生成时遵守字体纪律规则 |
| `taste.rules.color.*` | 配色 | 生成时遵守色彩约束规则 |
| `taste.rules.layout.*` | 布局 | 生成时遵守布局纪律规则 |
| `taste.rules.aiTells.*` | 内容 | 生成时遵守 AI 痕迹消除规则 |
| `taste.rules.image.*` | 图片 | 生成时遵守图片策略规则 |
| `taste.rules.buttons.*` | 按钮 | 生成时遵守按钮与内容规则 |
| `source.colors` | 配色 | 提取为设计 token 的颜色参数 |
| `source.style` | 调性 | 提取 styleId 匹配品牌模板库 |

**操作步骤：**
1. 检测用户消息中是否包含 taste JSON（特征：有 `taste.dials` 和 `taste.rules` 键）
2. 解析所有字段，在 Step 1 的总结中声明："已从 taste JSON 提取：动效=6/方差=7/密度=4，22 条规则全部启用"
3. 跳过被覆盖的维度询问，只问用途、媒体、时长等未被覆盖的维度
4. 在 Step 4 生成时严格按规则执行，在 Step 5 自检时将 taste 规则加入检查项

---

## Step 2 · 参考收集

用户可提供参考素材。处理策略见 `references/reference-extraction.md`。

**输入类型**：
- **项目内 DESIGN.md**（最高优先级）— 输出目录或项目根已有含托管区块的 `DESIGN.md` 时先读它：`<!-- DESIGN_MANAGED_START/END -->` 之间是上次生成的 tokens（同项目多页面防风格漂移的锚点），标记外是用户手写要求（优先级高于 tokens，直接并入本次约束）。机制见下方「设计规格持久化」
- **本地图片** — Read 工具读取，提取配色/字体/布局/组件
- **网页 URL** — WebFetch 抓取，提取 CSS 变量/配色/结构
- **设计稿** — 当作图片处理
- **混合** — 以图片为最高优先级，URL 次之，文字补充
- **品牌模板** — 从 `references/design-md/` 的 71 个品牌设计规格中选取（见下方品牌模板库）

**必须输出参考摘要表**：

```
配色：主色 #xxx / 辅色 #xxx / 背景 #xxx / 文字 #xxx
字体：标题用 xxx / 正文用 xxx / 强调用 xxx
布局：[单栏 | 双栏 | 网格 | 层叠 | 混合]
动效：[无 | subtle | 滚动驱动 | 全屏动画]
组件：导航栏、hero区、特性展示、CTA、footer...
调性关键词：[3-5 个词]
```

**必须询问用户确认**：「我从参考中理解到这些，对吗？需要调整什么？」

---

## Step 3 · 选技术栈 + 维度

### 技术栈

| 技术栈 | 适用场景 | CDN |
|--------|----------|-----|
| 原生 HTML/CSS/JS | 简单页面、海报、静态展示 | 无需引入 |
| Vue 3 CDN | 交互丰富、组件化、状态管理 | `https://unpkg.com/vue@3/dist/vue.global.prod.js` |
| React CDN | 复杂 UI、大量动态组件 | React + ReactDOM + Babel standalone |
| 框架 + Three.js | 3D 场景 + UI 交互 | 框架 CDN + Three.js importmap |

**选择逻辑**：
- 默认原生
- 需要 tab 切换/表单联动/动态列表 → Vue
- 用户说"用 React" → React
- 需要 3D → 框架 + Three.js
- 用户指定 → 直接遵从

Vue/React CDN 骨架模板见 `references/system-prompt-design.md`。

### 维度

自动匹配 6 维度：`form`（排版）、`motion`（动效）、`3D`、`media`（媒体）、`duration`（时长）、`style`（风格）

告知用户选了什么技术栈 + 哪些维度。

### 动效等级映射（来自 taste-picker 的 motionIntensity）

当用户提供了 taste JSON 中的 `motionIntensity` 值，按以下映射生成动效：

| 等级 | 名称 | 技术实现 | 适用场景 |
|------|------|----------|----------|
| 1-2 | 静态 | 仅 `:hover` / `:active` CSS 变换，无 transition | 严肃文档、政府、打印级页面 |
| 3-4 | 微动 | `transition: all 0.3s ease`，入场 `opacity 0→1`，hover `translateY(-2px)` | 极简落地页、博客、作品集 |
| 5-6 | 流体 | stagger 入场（delay cascade），hover `scale + shadow`，按钮 `:active scale(0.98)` | 标准 SaaS 落地页、品牌站 |
| 7-8 | 编排 | 滚动驱动动画（IntersectionObserver / scroll-driven CSS），视差背景，sticky pin | 高端品牌、创意机构、产品发布 |
| 9-10 | 电影级 | GSAP ScrollTrigger 全页编排，sticky-stack，横滚劫持，弹簧物理 | Awwwards 级作品集、实验站、活动页 |

**关键约束**：
- 等级 5 以下只用 CSS（`transition` / `animation` / `@keyframes`），不引入 JS 动画库
- 等级 7 以上必须引入 GSAP + ScrollTrigger（CDN），参考 taste-skill Section 5 的 canonical skeleton
- 所有等级必须尊重 `prefers-reduced-motion`：等级 5+ 必须 JS 检测并降级到静态
- 等级 3+ 的入场动画用 `cubic-bezier(0.16, 1, 0.3, 1)`（ease-out expo）
- 每个动画必须有理由（层级 / 叙事 / 反馈 / 状态切换），不为动效而动效

### 布局方差映射（来自 taste-picker 的 designVariance）

当用户提供了 taste JSON 中的 `designVariance` 值，按以下映射生成布局：

| 等级 | 名称 | 布局策略 | 具体做法 |
|------|------|----------|----------|
| 1-2 | 严格对称 | 12 列等分 CSS Grid，居中对齐 | 等宽列，等间距，所有元素居中。Hero 居中。卡片等高。 |
| 3-4 | 轻微偏移 | 标准网格，偶有重叠 | 基本对称，允许个别元素 `margin-top: -1rem` 或 `2fr 1fr` 不等分 |
| 5-6 | 适度不对称 | 混合比例，偏移布局 | `grid-template-columns: 2fr 1fr`，图片宽高比混合（4:3 旁 16:9），左对齐标题配居中数据 |
| 7-8 | 强烈不对称 | 大面积留白 + 紧凑区对比 | `padding-left: 20vw` 留白，`3fr 1fr` 比例，卡片大小差异明显，侧边大面积空 |
| 9-10 | 自由版式 | 瀑布流，极端比例 | CSS Grid `grid-template-columns: 2fr 1fr 1fr`，masonry 风格，元素重叠，巨大留白区 |

**关键约束**：
- 等级 4 以下：Hero 居中可以接受
- 等级 5 以上：Hero 必须非居中（分屏 / 左对齐 / 不对称）
- 所有等级在 `< 768px` 必须折叠为单列 `w-full px-4`

### 视觉密度映射（来自 taste-picker 的 visualDensity）

当用户提供了 taste JSON 中的 `visualDensity` 值，按以下映射控制间距和信息量：

| 等级 | 名称 | 间距 | 字号 | 信息量 |
|------|------|------|------|--------|
| 1-2 | 画廊级 | `py-32` 到 `py-48`，section gap 128px+ | 标题大，正文 16px | 每屏 1-2 个核心信息 |
| 3-4 | 标准 | `py-16` 到 `py-24`，section gap 64-96px | 标题正常，正文 15-16px | 每屏 2-4 个信息块 |
| 5-6 | 紧凑 | `py-12`，section gap 48px | 标题略小，正文 14px | 每屏 4-6 个信息块 |
| 7-8 | 密集 | `py-8`，section gap 32px，`gap-4` | 正文 13-14px，用 `divide-y` 分隔 | 每屏 6-10 个项目 |
| 9-10 | 仪表盘 | `py-4`，`gap-2`，1px 分割线 | 数字用 `font-mono`，正文 12-13px | 最大化信息密度，无装饰边距 |

**关键约束**：
- 等级 5 以上：卡片容器尽量不用，改用 `border-t` / `divide-y` / 纯负空间分组
- 等级 7 以上：数字必须用等宽字体
- 所有密度等级都要保持可读性：正文最小 12px，行高至少 1.5

**taste JSON 中的规则约束**：
- `taste.rules.aiTells.emDashBan` — 页面中不使用破折号
- `taste.rules.typography.banInterDefault` — 不用 Inter 作默认字体
- `taste.rules.color.noAiPurple` — 不用 AI 紫色渐变
- `taste.rules.color.oneAccentLock` — 全页锁定单一强调色
- 其他规则按 taste-skill 的 Pre-Flight Check 执行

### 品牌模板库

`references/design-md/` 包含 71 个品牌设计规格（来自 awesome-design-md），每个文件定义了完整的配色、字体、间距、组件等设计 token。

**使用方式**：
- 用户提到某个品牌或风格（如"做成 Stripe 那种"、"像 Apple 官网"）→ 读取对应的 `references/design-md/<brand>/DESIGN.md`，提取设计 tokens 作为参考
- 用户没有指定 → 根据调性/维度自动匹配最接近的 1-3 个品牌模板，告知用户选择
- 可与用户提供的参考图/URL 叠加使用

**可用品牌**：airbnb, airtable, apple, binance, bmw, bmw-m, bugatti, cal, claude, clay, clickhouse, cohere, coinbase, composio, cursor, elevenlabs, expo, ferrari, figma, framer, hashicorp, ibm, intercom, kraken, lamborghini, linear.app, lovable, mastercard, meta, minimax, mintlify, miro, mistral.ai, mongodb, nike, notion, nvidia, ollama, opencode.ai, pinterest, playstation, posthog, raycast, renault, replicate, resend, revolut, runwayml, sanity, sentry, shopify, slack, spacex, spotify, starbucks, stripe, supabase, superhuman, tesla, theverge, together.ai, uber, vercel, vodafone, voltagent, warp, webflow, wired, wise, x.ai, zapier

### 幻灯片模板库

`C:\Users\lenovo\.claude\skills\slide-deck\templates\` 包含 34 套精心设计的 HTML 幻灯片模板，每套含 `template.json`（元数据+配色+字体）和 `design.md`（完整设计系统文档）。

**使用方式**：
- 当用户需求是幻灯片/演示/PPT 风格页面 → 提示用户使用 `slide-deck` skill
- 当用户需求是普通页面但需要灵感 → 读取某个模板的 `design.md` 提取配色/字体/间距 tokens 作为参考
- `index.json` 包含所有模板的 mood/tone/occasion/formality 元数据，可按调性匹配

---

## Step 4 · 生成（Actor）

**硬约束**：
- 禁止 Unsplash/picsum 占位图
- 禁止 Lorem ipsum 占位文案
- 禁止 `href="#"` 空链接
- 禁止 alert/prompt/confirm
- 禁止未定义的 CSS 变量
- 禁止 npm/webpack/vite build 步骤

**必须**：
- 输出完整 `<!DOCTYPE html>...</html>`
- 所有 CSS 在 `<style>` 内
- 所有 JS 在 `<script>` 内
- 图片用 base64 data URL 内嵌（如有用户提供）
- 字体从 Google Fonts 加载
- CSS 变量全部在 `:root` 定义
- 使用语义 HTML5

**反 AI slop**：
- 禁止字体三件套：Inter + 紫色渐变 + Space Grotesk
- 禁止 Tailwind 默认蓝色 (#3B82F6)
- 配色必须有主导色（不是均匀分布）
- 布局必须打破常规网格（非对称、层叠、或有意的大留白）
- 背景禁止纯色平面（必须分层：渐变/噪点/图案/光晕）

输出到 `output/<页面名>/index.html`

---

## Step 5 · Actor-Critic 自评

### 5a. 自检（Actor 自己做）

扫描生成结果，过一票否决清单（V-01 ~ V-06，见 `references/quality-rubric.md`）：
- broken image → 修复
- 空链接 → 加真实锚点或移除
- 占位文案 → 替换为真实内容
- 未定义 CSS 变量 → 补定义
如有命中，**直接修复**，不进 critic。

### 5a-taste. taste 规则自检（仅在 taste JSON 存在时）

如果用户提供了 taste JSON，在 5a 之后额外扫描以下规则。每条规则如命中则**直接修复**：

**typography（字体纪律）：**
- `banInterDefault=true` → 检查 `font-family` 中是否以 Inter 开头，替换为 Geist/Satoshi/Outfit
- `banFrauncesInstrumentSerif=true` → 检查是否加载了 Fraunces 或 Instrument Serif，替换
- `serifOnlyWhenJustified=banned/discouraged` → 检查是否有衬线字体，如 banned 则全部替换为无衬线

**color（色彩校准）：**
- `noAiPurple=true` → 检查是否有 `#7c3aed` `#a855f7` `#6366f1` 系紫色渐变，替换为非紫强调色
- `noPremiumConsumerBeigeBrass=true` → 检查是否 `#f5f1ea` 系暖米背景 + `#b08947` 系黄铜强调，替换
- `oneAccentLock=true` → 检查页面中使用的强调色是否超过 1 个色系，统一为单色

**layout（布局纪律）：**
- `eyebrowLimit=true` → 统计 `uppercase tracking` 类标签数量，超过 `ceil(section数/3)` 则删除多余的
- `antiCenterHero=true` → 如方差 > 4 且 Hero 居中，改为分屏或左对齐

**aiTells（AI 痕迹消除）：**
- `emDashBan=strict` → 搜索 `—` 和 `–`，全部替换为连字符或删除
- `noFakeData=true` → 检查是否有 `99.99%`、`10x`、`12345` 类虚假精确数字
- `noDivFakeScreenshots=true` → 检查是否有 div 矩形模拟产品截图
- `noGenericNames=true` → 检查是否有 Jane Doe / Sarah / John 类占位名

**image（图片策略）：**
- `requireRealImages=true` → 检查是否所有图片区域都有真实 src（非空/非占位 div）
- `noPlaceholderDivs=true` → 检查是否有纯色块代替图片

**buttons（按钮与内容）：**
- `contrastCheck=true` → 检查按钮文字与背景的对比度（目测是否白字白底）
- `noWrap=true` → 检查按钮文字是否在桌面端换行
- `noDuplicateIntent=true` → 检查是否有两个 CTA 表达同一意图（如"联系我们"+"取得联系"）
- `heroWordLimits=true` → 检查 Hero 副标题是否超过 20 字/词

### 5b. 独立 Critic（sub-agent）

启动 Agent sub-agent（subagent_type: general-purpose）：

**Critic prompt**：
```
You are the critic — independent of the generator.
Score the HTML against the quality rubric (R-01 → R-20, V-01 → V-06).
{如有 taste JSON，追加：Also check these taste rules: {taste.rules 的 JSON}}
Be conservative: assume the generator inflated 0.4 ~ 0.75.
Return ONLY JSON:
{"score": <number>, "gaps": ["ID 具体问题"], "ship": <boolean>, "veto_hit": <string|null>}

HTML to evaluate:
{截取前 10000 字符的 HTML}
```

**评分标准**：见 `references/quality-rubric.md`
**评分范围**：0-5，0.05 步进
**ship 条件**：score ≥ 3.5 且无 veto 命中

### 5c. 迭代决策

```
if ship=false AND score < 3.5 AND iteration < 2:
    把 gaps 列表附加到下一轮生成的 prompt 中
    iteration += 1
    回到 Step 4 重新生成
else:
    进入 Step 6 交付
```

最多 2 轮迭代。每轮告知用户当前分数和 gaps。

---

## Step 6 · 交付

- 确认文件写入 `output/<页面名>/index.html`
- 写入 `DESIGN.md` 设计规格（见下方「设计规格持久化」）
- 告知：「双击即可在浏览器打开」
- 可选提示部署：Cloudflare Pages / GitHub Pages / Netlify Drop
- 如有需要，告知如何修改文案或配色

---

## 设计规格持久化（DESIGN.md 托管区块）

每次生成页面，同步在输出目录（同项目多页面时放项目根或 `output/` 上级，全项目共用一份）写 `DESIGN.md`，结构固定：

```
<!-- DESIGN_MANAGED_START -->
colors: 主色/辅色/背景/文字/强调 各 hex
typography: 标题/正文/等宽字体 + 字号阶梯
spacing: 间距阶梯
motion: 动效等级 + 实际使用的效果
hard_rules: 本次生效的硬约束（单一强调色锁定、禁 Inter 默认、命中的反 AI slop 项、taste 规则）
source: 设计来源（taste JSON / 品牌模板名 / 参考图 URL 摘要）
<!-- DESIGN_MANAGED_END -->

（标记之外是用户手写备注区，任意内容）
```

**更新规则**：
- 托管区块 = 机器生成区。改版/加页面时**只替换两个标记之间的内容**，标记外一个字不动
- 用户在标记外手写的设计要求，优先级**高于**托管区块内的 tokens
- 文件已存在但**没有标记** → 视为纯用户文件，禁止覆盖；如需追加托管区块，先在文件末尾追加并告知用户
- 更新托管区块时，如果 tokens 实际没变（只是改文案），不重写，保持原生成时间

## Reference Files

| 文件 | 用途 |
|------|------|
| `references/quality-rubric.md` | 评分量表（R-01→R-20，V-01→V-06） |
| `references/actor-critic.md` | Actor-Critic 循环模式详解 |
| `references/system-prompt-design.md` | Prompt 设计原则 + Vue/React CDN 模板 |
| `references/reference-extraction.md` | 从图片/URL 提取设计 tokens |
| `references/sse-streaming.md` | SSE 流式解析模式（浏览器端工具用） |
| `references/design-md/` | 71 个品牌设计规格模板（awesome-design-md），按品牌名分目录 |

需要深入某个模式时，读取对应的 reference 文件。
