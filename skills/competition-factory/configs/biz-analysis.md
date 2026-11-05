# Business Analysis Competition Config

## Roles

| Role | Responsibility | Subagent Focus |
|------|---------------|----------------|
| **Industry Researcher** | 行业研究、市场规模、趋势分析 | Web search + data aggregation |
| **Data Analyst** | 数据清洗、统计分析、可视化 | Python (pandas/matplotlib/plotly) |
| **Strategist** | 竞争策略、商业模式设计 | Framework-driven analysis |
| **Financial Modeler** | 财务预测、投资回报、估值 | Excel/Python financial models |
| **Report Writer** | 撰写商业分析报告 | Structured writing per template |
| **Reviewer** | 审查逻辑一致性、数据准确性 | Checklist-based QA |

## Pipeline

```
1. Industry Scan      → 行业概览、市场规模、增长趋势
2. Problem Framing    → 明确分析目标、拆解子问题
3. Data Collection    → 爬取/收集行业数据、公司财报
4. Market Analysis    → 市场规模(TAM/SAM/SOM)、细分市场、增长驱动因素
5. Competitive Landscape → 竞品分析、波特五力、市场定位图
6. Strategy Design    → 商业模式设计、增长策略、差异化定位
7. Financial Model    → 收入预测、成本结构、ROI/NPV/IRR
8. Risk Analysis      → 风险识别、影响评估、应对策略
9. Report Writing     → 按模板撰写完整报告
10. Slide Generation  → 生成演示PPT（可选）
```

## Output Format

### 商业分析报告结构
```
封面（题目、团队信息）
目录

一、执行摘要（1-2页）
├── 核心发现
├── 关键建议
└── 预期影响

二、行业背景与市场分析
├── 行业概况
├── 市场规模与增长
├── 市场细分
└── 趋势与驱动因素

三、竞争格局分析
├── 波特五力分析
├── 主要竞争者对比
├── 市场定位图
└── 竞争优势分析

四、目标用户分析
├── 用户画像
├── 需求痛点
├── 用户旅程
└── 市场机会

五、商业模式与策略
├── 商业模式画布
├── 收入模式
├── 增长策略
└── 运营策略

六、财务分析
├── 收入预测（3-5年）
├── 成本结构
├── 盈亏平衡分析
├── ROI/NPV/IRR
└── 敏感性分析

七、风险评估与应对
├── 市场风险
├── 运营风险
├── 财务风险
└── 风险矩阵与应对策略

八、结论与建议

附录（数据来源、计算过程、代码）
```

## Domain References

Read `references/biz-frameworks.md` for detailed framework guides.

## Actor-Critic Rules
- **Industry Research**: 2 rounds (accuracy check)
- **Financial Model**: 3 rounds (numbers must be consistent across sections)
- **Report Writing**: 2 rounds (logic flow, evidence backing)
- **Final Review**: 1 round (completeness check)

## Key Differences from Math Modeling
- Web research is critical (use WebSearch tool)
- Data may not be provided — need to find/scrape
- Output is a business report, not academic paper
- Charts should be business-style (not academic)
- Financial projections require clear assumptions documented
- May need to generate PPT slides (use guizang-ppt-skill)

## Full Skill
This config delegates to `biz-analysis-pro` for the complete pipeline:
- 12-stage workflow with 6 specialist subagents
- Industry research with web search + source citation
- Market sizing (TAM/SAM/SOM) with multiple calculation methods
- Competitive landscape (Porter's 5 Forces + positioning map)
- Financial projection script (`biz-analysis-pro/scripts/financial_model.py`)
- 7 business chart templates (waterfall, positioning, funnel, risk matrix, etc.)
- Business report template
- Self-review rubric (10-point checklist)
