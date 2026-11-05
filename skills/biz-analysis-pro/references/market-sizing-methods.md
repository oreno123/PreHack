# Market Sizing Methods

## Three Approaches

### 1. Top-Down (自上而下)
Start from total market → narrow down to target segment.

```
TAM = 行业总规模 × 目标渗透率上限
SAM = TAM × 地域/渠道可及比例
SOM = SAM × 现实可获份额（考虑竞争、资源、时间）

Example:
中国餐饮市场规模 (2024) = ¥5.7万亿 [国家统计局]
  × 火锅品类占比 = 13.5% [美团餐饮报告 2024]
  = 火锅市场 TAM = ¥7,695亿
  × 一二线城市占比 = 55%
  = 一二线火锅 SAM = ¥4,232亿
  × 5年可获份额 = 3%
  = 目标 SOM = ¥127亿
```

**Sources for top-down:**
- 国家统计局 (stats.gov.cn)
- 艾瑞咨询 (iresearch.cn) — 互联网/科技
- 易观分析 (analysys.cn) — 互联网行业
- 前瞻产业研究院 (qianzhan.com) — 传统行业
- 欧睿国际 (euromonitor.com) — 消费品
- Frost & Sullivan — 多行业
- 上市公司年报/招股书 — 具体品类数据

### 2. Bottom-Up (自下而上)
Start from unit economics → build up to total.

```
SAM = 目标用户数 × 渗透率 × ARPU × 12 (月)

Example: 在线英语教育
中国K12学生 = 1.8亿 [教育部]
  × 有课外英语辅导需求的比例 = 25%
  × 愿意尝试在线的比例 = 40%
  = 目标用户 = 1800万
  × 付费转化率 = 8%
  = 付费用户 = 144万
  × 年均付费 = ¥8,000
  = SAM = ¥115亿
```

**Key parameters to research:**
- 目标人群总数 → 人口统计、行业统计
- 渗透率 → 参考成熟市场或类比行业
- ARPU → 竞品定价、用户调研
- 付费率 → 行业benchmark

### 3. Value Theory (价值推算法)
Estimate from value created for users.

```
市场规模 = 使用场景价值 × 使用频率 × 可触达用户数

Example: 企业协作SaaS
每个企业员工每天在沟通协作上浪费 1.5 小时
  × 每小时成本 ¥50（白领平均时薪）
  = 每人每天浪费 ¥75
  × 250 工作日 = 每人每年 ¥18,750
如果工具能节省 30% = 每人每年创造价值 ¥5,625
  × 中国白领人数 1.2亿
  × 愿意为工具付费的比例 15%
  = 市场规模 = ¥1,012亿
```

## Cross-Validation

Always use at least 2 methods and compare:

```
Top-down result: ¥120亿
Bottom-up result: ¥95亿
Gap: 26%

If gap > 50%, recheck assumptions.
Document the range: ¥95-120亿 (base case)
```

## Growth Rate Estimation

```
CAGR = (End Value / Start Value) ^ (1/Years) - 1

Sources:
- 历史数据算 CAGR (过去3-5年)
- 行业报告预测
- 类比成熟市场 (同品类在发达国家的发展轨迹)
- 专家访谈/新闻

Always give range:
- Conservative: 历史CAGR × 0.7
- Base: 历史CAGR
- Optimistic: 历史CAGR × 1.3
```

## Formatting in Report

Always present as:

| 指标 | 保守 | 基准 | 乐观 | 来源 |
|------|------|------|------|------|
| TAM | ¥X亿 | ¥Y亿 | ¥Z亿 | [来源1, 2024] |
| SAM | ... | ... | ... | 计算得出 |
| SOM | ... | ... | ... | 计算得出 |
| CAGR | A% | B% | C% | [来源2, 2024] |
