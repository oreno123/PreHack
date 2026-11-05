# Business Analysis Frameworks Quick Reference

## Market Sizing
### TAM/SAM/SOM
```
TAM (Total Addressable Market) = 整个市场总规模
SAM (Serviceable Available Market) = 你能服务的市场子集
SOM (Serviceable Obtainable Market) = 你现实能拿到的份额

计算方法：
1. Top-down: 行业报告数据 → 逐步缩小
2. Bottom-up: 目标用户数 × 付费率 × ARPU × 12月
3. Value Theory: 使用场景价值 × 使用频率 × 目标人数
```

## Industry Analysis
### Porter's Five Forces (波特五力)
| Force | Key Questions |
|-------|--------------|
| 供应商议价能力 | 供应商集中度？替代品多少？转换成本？ |
| 买方议价能力 | 买方集中度？价格敏感度？替代品多少？ |
| 新进入者威胁 | 进入壁垒？规模经济？品牌壁垒？政策壁垒？ |
| 替代品威胁 | 替代品性能价格比？转换成本？替代趋势？ |
| 行业竞争强度 | 竞争者数量？行业增长率？产品差异化？退出壁垒？ |

### PESTEL Analysis
| Dimension | 分析要点 |
|-----------|---------|
| Political | 政策支持/限制、监管环境、贸易政策 |
| Economic | GDP增长、通胀、利率、消费能力 |
| Social | 人口结构、消费习惯、文化因素 |
| Technological | 技术成熟度、创新速度、数字化程度 |
| Environmental | 环保法规、可持续发展、ESG |
| Legal | 法律法规、知识产权、合规要求 |

## Strategy
### SWOT Analysis
| | Positive | Negative |
|---|---|---|
| **Internal** | Strengths (优势) | Weaknesses (劣势) |
| **External** | Opportunities (机会) | Threats (威胁) |

关键：SO策略（利用优势抓住机会）、WO策略（克服劣势抓住机会）、ST策略（利用优势规避威胁）、WT策略（减少劣势规避威胁）

### Business Model Canvas (商业模式画布)
```
┌──────────┬──────────┬──────────┬──────────────────┐
│Key       │Key       │Value     │Customer          │
│Partners  │Activities│Proposition│Relationships    │
│          ├──────────┤          ├──────────────────┤
│          │Key       │          │Customer          │
│          │Resources │          │Segments          │
├──────────┴──────────┼──────────┼──────────────────┤
│   Cost Structure    │   Revenue Streams           │
└─────────────────────┴─────────────────────────────┘
```

### Ansoff Matrix (安索夫矩阵)
| | 现有产品 | 新产品 |
|---|---|---|
| **现有市场** | 市场渗透 | 产品开发 |
| **新市场** | 市场开发 | 多元化 |

## Growth
### AARRR (Pirate Metrics)
```
Acquisition (获客) → Activation (激活) → Retention (留存) → Revenue (收入) → Referral (传播)

关键指标：
- 获客成本 (CAC)
- 激活率 (Activation Rate)
- 留存率 (D1/D7/D30 Retention)
- ARPU / LTV
- 病毒系数 (K-factor)
```

### Unit Economics (单位经济)
```
LTV = ARPU × 平均生命周期 × 毛利率
CAC = 总获客成本 / 新增用户数
LTV/CAC > 3 是健康的
回本周期 = CAC / (ARPU × 毛利率)
```

## Financial
### Revenue Projection
```python
# 简单收入预测模型
users_month_0 = initial_users
growth_rate = 0.10  # 月增长10%
churn_rate = 0.05   # 月流失5%
arpu = 50           # 月ARPU

users = []
for month in range(36):
    new_users = users[-1] * growth_rate if users else users_month_0
    lost_users = (users[-1] if users else users_month_0) * churn_rate
    current = (users[-1] if users else users_month_0) + new_users - lost_users
    users.append(current)

revenue = [u * arpu for u in users]
```

### Break-even Analysis
```
盈亏平衡点 = 固定成本 / (单价 - 单位变动成本)
```

### NPV / IRR
```python
import numpy as np
cashflows = [-1000000] + [250000] * 5  # 初始投资 + 5年现金流
npv = np.npv(0.1, cashflows)  # 10% 折现率
irr = np.irr(cashflows)
```

## Risk
### Risk Matrix
```
         │ Low Impact │ Med Impact │ High Impact │
─────────┼────────────┼────────────┼─────────────┤
High Prob│   Monitor  │ Mitigate   │   Avoid     │
Med Prob │   Accept   │ Mitigate   │   Transfer  │
Low Prob │   Accept   │  Accept    │   Monitor   │
```

## Visualization Types for Business Reports
| 分析类型 | 推荐图表 |
|---------|---------|
| 市场规模 | 瀑布图、堆叠柱状图 |
| 市场份额 | 饼图/环形图、treemap |
| 增长趋势 | 折线图、面积图 |
| 竞品对比 | 雷达图、气泡图 |
| 用户画像 | 柱状图、漏斗图 |
| 财务预测 | 组合图（柱+线） |
| 风险矩阵 | 散点图（热力） |
| 流程/旅程 | 漏斗图、Sankey图 |
