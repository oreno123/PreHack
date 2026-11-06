# API 速查（国产模型 / 免费档 / 链上数据 / 代理选路）

> key 一律走环境变量，本文不含任何密钥。

## 智谱 bigmodel（免费档主力）

- Base：`https://open.bigmodel.cn/api/paas/v4`
- **glm-4v-flash = 免费视觉问答**：`chat/completions` 传 `image_url`（base64 内嵌即可），零成本做 VLM 打分/选片。glm-4v-plus 是收费档，别混用
- **cogview-3-flash = 唯一免费生图**（`images/generations`，返回 `data[0].url` 直接下载）：1-2 秒出图，带"AI生成"水印
  - 防跑偏三板斧：风格词前置句首 + 显式负面词（无人物/无照片感）+ 明确几何约束（正圆形、居中）
  - 上限认知：复杂对称结构（严格八重对称+回纹边框）三轮重试不可达，是模型上限不是 prompt 问题

## StepFun（Step Plan 套餐）

- 前缀：`https://api.stepfun.com/step_plan/v1/...`，OpenAI 兼容格式
- **step-3.7-flash 是套餐里唯一支持图片输入的**（3.5 调图报 `model_incompatible`）
- reasoning 模型三坑：
  - `content` 经常是空串，真实输出在 `reasoning_content`/`reasoning`——读取做三级 fallback
  - `max_tokens` 给 4000+，否则思考链没跑完就被截断
  - 输出 JSON 字段名被污染（`score{`、`verdict{`），解析前做字段名归一化
- **结构化输出用包裹器**：prompt 强制 `<<<JSON>>>{...}<<<END>>>`，正则提取，比 ```json``` 代码块稳
- **想让模型"拒绝"时用判定门，别用例外条款**：强制第一行输出 `判定：是|否`，解析端判"否"就无条件丢弃后续。"若图中没有X则答无"这类例外条款会被无视（实测两连败）

## 链上数据（以太坊主网）

| 需求 | 端点 | 要点 |
|---|---|---|
| 事件日志 getLogs | `ethereum-rpc.publicnode.com` | 块范围上限 ~5000，step 2000-4000 分片 |
| 历史 eth_call (archive) | `eth-mainnet.public.blastapi.io` | publicnode 历史块返 403，读历史走 blastapi |
| 任意范围日志 | `eth.blockscout.com/api` | 双 topic 过滤参数名必须匹配：跳过 topic1 时用 `topic0_2_opr`，写错**静默失效**；易 429 慎用 |
| 价格 | `coins.llama.fi/prices/current/{chain}:{addr}` | 单 URL ~15 地址，超长返空须分块 |
| 协议 TVL | `api.llama.fi/protocol/{slug}` | Aave 的"TVL"=净可用流动性（存−借），不是存款总量 |

- 不可用名单（实测挂）：rpc.ankr.com（SSL EOF）、eth.llamarpc.com（525）

## 代理与墙

- 本机 Clash HTTP 代理端口 **7897**（7890 不通）：`curl -x http://127.0.0.1:7897 ...`
- 国内目标（CCTV CDN、国产 API）**别挂代理**，挂了反而失败；被墙目标（archive.org、Met Museum API、Wikimedia）直连超时走代理
- 出口验证：`curl -x ... https://ipinfo.io/json`

## 通则

- reasoning 模型（gpt-5/step-3.7）通用：max_tokens 4000+，content 空就查 reasoning 字段
- rate limit 用多模型轮换 + sleep(1-3)，别硬顶单模型
