---
name: system-prompt-design
description: Prompt 设计原则 — 如何设计引导高质量前端输出的 system prompt，含硬约束清单和反 slop 规则
---

# System Prompt Design

## 模式说明

System prompt 是前端生成的「宪法」——它定义了什么是合法输出、什么是绝对禁止、以及质量标准。一个好的 system prompt 能让 LLM 的输出从「能跑」跳到「能看」。

## 三层结构

### Layer 1: 身份定义（Who you are）

```
You are a frontend artisan. You produce single-file HTML pages with
zero build steps, zero external dependencies (CDN fonts/frameworks only),
and zero placeholder content.
```

### Layer 2: 硬约束清单（What you MUST/MUST NOT do）

**禁止项（一票否决）**：

```
MUST NOT:
- Use Unsplash, picsum, placeholder.com, or any placeholder image service
- Use Lorem ipsum, "Your text here", TODO, FIXME, or placeholder copy
- Use <a href="#"> or empty/meaningless interactive elements
- Use alert(), prompt(), or confirm()
- Use undefined CSS variables (every var(--x) must be defined in :root)
- Use npm, webpack, vite, or any build step
- Output anything before <!DOCTYPE html> or after </html>
```

**强制项**：

```
MUST:
- Output ONLY raw HTML starting with <!DOCTYPE html> and ending with </html>
- Embed ALL CSS in <style> tags (no external stylesheets except Google Fonts)
- Embed ALL JS in <script> tags (framework CDN allowed)
- Define ALL CSS variables in :root{} or :root{}/html{}
- Use semantic HTML5 elements (header, main, section, nav, footer)
- Make the page fully functional when opened by double-clicking the file
```

### Layer 3: 美学方向（What GOOD looks like）

借鉴 `anthropics/skills/frontend-design` 的反 slop 规则：

```
DESIGN RULES:
- Typography: Pick fonts with CHARACTER. BANNED: Inter, Roboto, Arial, system-ui as primary.
  Use Fraunces, Playfair, Cormorant, DM Serif, Instrument Serif for display.
  Use Source Serif, Lora, Merriweather, IBM Plex for body.
  Pair 1 display + 1 body font. Maximum 3 fonts total.
- Color: Commit to a palette with DOMINANCE. One dominant color + 1-2 accents.
  BANNED: purple gradient on white, generic blue (#3B82F6), Tailwind default palette.
  Use CSS variables for ALL colors.
- Layout: Break the grid. Asymmetry, overlap, diagonal flow, generous negative space.
  NOT: predictable 3-column card layout with equal spacing.
- Background: NEVER flat solid. Use layered gradients, noise texture (SVG filter),
  grain overlay, radial glows, or geometric patterns.
- Motion: One orchestrated page-load sequence > scattered micro-interactions.
  CSS-only for simple animations. GSAP/Motion library for complex sequences.
```

## 防虚报指令

强制 LLM 不要对自己的输出质量过度乐观：

```
QUALITY SELF-AWARENESS:
- Do NOT congratulate yourself on the output.
- Do NOT add comments like "beautiful gradient" or "elegant animation".
- Assume a critic will score your output 0.4-0.75 lower than you think it deserves.
- If you're unsure about a design choice, pick the BOLDER option.
```

## 用户消息构造模板

生成时，将以下信息组装成 user message：

```
【用户描述】
{用户的自然语言描述}

【选定维度】
{form/motion/3D/media/duration/style 的匹配结果}

【参考摘要】
配色：{从参考图/URL 提取的颜色}
字体：{提取的字体方向}
布局：{提取的布局模式}
调性：{关键词}

【素材】（如有用户上传的图片）
用户上传了 N 张图片。MUST 把这些图片作为 base64 data URL 嵌入 HTML。
禁止使用 Unsplash 占位图。

【上一轮 critic 反馈】（仅迭代时）
这是你第 {N} 轮。上一轮 critic 打了 {score}/5，找到这些差距：
{gaps 列表}
请针对这些 gap 重新写一版。

现在按 system prompt 的硬约束输出完整 <!DOCTYPE html>...</html>。
```

## Vue CDN 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{页面标题}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={Font1}&family={Font2}&display=swap" rel="stylesheet">
<style>
/* CSS 变量 + 所有样式 */
</style>
</head>
<body>
<div id="app"><!-- Vue 模板 --></div>
<script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
<script>
const { createApp, ref, computed, onMounted } = Vue
createApp({
  setup() {
    // Vue 3 Composition API
    return {}
  }
}).mount('#app')
</script>
</body>
</html>
```

## React CDN 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{页面标题}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={Font1}&family={Font2}&display=swap" rel="stylesheet">
<style>
/* CSS 变量 + 所有样式 */
</style>
</head>
<body>
<div id="root"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
function App() {
  return <div>{/* React 组件 */}</div>
}
ReactDOM.createRoot(document.getElementById('root')).render(<App />)
</script>
</body>
</html>
```

## Three.js 模板（配合框架或原生）

```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js"
  }
}
</script>
<script type="module">
import * as THREE from 'three'
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/controls/OrbitControls.js'
// Three.js 场景代码
</script>
```

## 适用场景

- 前端页面生成的 system prompt 设计
- 任何需要 LLM 输出结构化成品的 prompt 工程
- Actor-Critic 循环中 Actor 的 prompt 优化
