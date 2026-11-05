---
name: sse-streaming
description: SSE 流式解析模式 — 浏览器端手动解析 Anthropic SSE 流，适用于任何 BYOK 直连 AI API 的工具
---

# SSE Streaming Pattern

## 模式说明

当浏览器端工具直接调用 Anthropic API 时，使用 `stream: true` 获取 Server-Sent Events (SSE) 响应。这允许边生成边展示进度，而不是等整个响应完成。

注意：本模式仅适用于浏览器端 BYOK 工具。Claude Code skill 本身不需要 SSE（Claude 直接生成）。

## 核心代码（源自 ip-website-studio builder.js）

### 请求配置

```javascript
const API_URL = 'https://api.anthropic.com/v1/messages';
const MODEL = 'claude-sonnet-4-6';
const ANTHROPIC_VERSION = '2023-06-01';

const response = await fetch(API_URL, {
  method: 'POST',
  headers: {
    'x-api-key': userApiKey,
    'anthropic-version': ANTHROPIC_VERSION,
    'anthropic-dangerous-direct-browser-access': 'true',
    'content-type': 'application/json',
  },
  body: JSON.stringify({
    model: MODEL,
    max_tokens: 16000,
    stream: true,
    system: systemPrompt,
    messages: [{ role: 'user', content: contentBlocks }],
  }),
});
```

关键 header：`anthropic-dangerous-direct-browser-access: true` — 允许浏览器直接调用 API（绕过 CORS）。

### SSE 流解析

```javascript
const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = '';
let fullText = '';

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  buffer += decoder.decode(value, { stream: true });

  // 按换行拆分，保留最后一段未完成的
  const lines = buffer.split('\n');
  buffer = lines.pop() || '';

  for (const line of lines) {
    if (!line.startsWith('data: ')) continue;
    const data = line.slice(6).trim();
    if (!data || data === '[DONE]') continue;

    try {
      const evt = JSON.parse(data);
      if (evt.type === 'content_block_delta' && evt.delta?.type === 'text_delta') {
        fullText += evt.delta.text;
        updateProgress(fullText.length);
      }
    } catch (e) {
      // 跳过无法解析的行
    }
  }
}
```

### 进度映射（字节 → 步骤）

```javascript
function advanceProgressByBytes(charCount) {
  let step = 1;
  if (charCount > 4000) step = 2;
  if (charCount > 8000) step = 3;
  if (charCount > 12000) step = 4;
  setProgressStep(step);
}
```

### 中断支持

```javascript
const abortController = new AbortController();
fetch(API_URL, { signal: abortController.signal, ... });
abortController.abort(); // 用户取消时
```

## SSE 事件类型速查

| 事件类型 | 含义 | 处理方式 |
|----------|------|----------|
| `message_start` | 消息开始 | 提取 message id |
| `content_block_start` | 内容块开始 | 记录 block index |
| `content_block_delta` | 内容增量 | **核心** — 提取 `delta.text` 拼接 |
| `content_block_stop` | 内容块结束 | 无需特殊处理 |
| `message_delta` | 消息级更新 | 提取 `stop_reason` |
| `message_stop` | 消息结束 | 标记完成 |

## 多模态内容块

当需要发送图片时：

```javascript
const contentBlocks = [];

images.forEach(img => {
  contentBlocks.push({
    type: 'image',
    source: {
      type: 'base64',
      media_type: img.mediaType,
      data: img.base64,
    },
  });
});

contentBlocks.push({ type: 'text', text: userPrompt });
```

## 适用场景

- 浏览器端 BYOK 工具（如 ip-website-studio 的 builder）
- Electron 桌面应用调 Anthropic API
- 任何需要流式展示 AI 生成进度的前端工具
