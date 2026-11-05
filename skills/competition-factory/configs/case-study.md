# Case Study Competition Config (案例大赛)

## Roles

| Role | Responsibility |
|------|---------------|
| **Industry Analyst** | 行业背景研究、宏观环境分析 |
| **Diagnostician** | 企业问题诊断、根因分析 |
| **Solution Architect** | 解决方案设计、实施路径规划 |
| **Implementation Planner** | 执行计划、时间线、资源分配 |
| **Report Writer** | 咨询报告撰写 |
| **Reviewer** | 审查分析深度、方案可行性 |

## Pipeline

```
1. Case Intake         → 案例材料精读、关键信息提取
2. Background Research → 企业/行业背景调研
3. Problem Diagnosis   → 现状分析、问题识别、MECE拆解
4. Root Cause Analysis → 根因挖掘、Issue Tree构建
5. Solution Design     → 方案设计、可行性论证
6. Implementation Plan → 分阶段执行计划、时间线
7. KPI & Metrics       → 效果评估指标、监控方案
8. Risk Mitigation     → 风险识别、应急预案
9. Report Writing      → 咨询风格报告
10. Presentation       → 演示材料（可选）
```

## Output Format

### 咨询报告结构
```
一、执行摘要
二、案例背景
├── 企业概况
├── 行业背景
└── 核心挑战
三、现状分析
├── 外部分析（PESTEL/波特五力）
├── 内部分析（价值链/7S模型）
└── SWOT综合分析
四、问题诊断
├── 核心问题定义
├── Issue Tree（问题拆解）
└── 根因分析
五、解决方案
├── 方案一：[名称]
│   ├── 具体措施
│   ├── 预期效果
│   └── 所需资源
├── 方案二：[名称]
└── 方案推荐与对比
六、实施计划
├── 分阶段路线图
├── 关键里程碑
├── 资源需求
└── 时间线（甘特图）
七、效果评估
├── KPI设计
├── 监控机制
└── 预期成果
八、风险与应对
附录（数据支撑、分析工具）
```

## Actor-Critic Rules
- **Problem Diagnosis**: 3 rounds (MECE completeness check)
- **Root Cause**: 2 rounds (depth check — is this real root cause or symptom?)
- **Solution Design**: 3 rounds (feasibility + impact check)
- **Report**: 2 rounds

## Key Frameworks
- MECE (Mutually Exclusive, Collectively Exhaustive)
- Issue Tree (问题树)
- PESTEL Analysis
- Porter's Value Chain
- McKinsey 7S Model
- BCG Matrix
- Ansoff Matrix
- Force Field Analysis

## Style Notes
- Write like a consultant, not a student
- Every recommendation must be actionable (具体到谁做什么、什么时候做、怎么做)
- Use consulting-style charts (waterfall, bridge, 2x2 matrix)
- Prioritize insights over data dump
- Executive summary should stand alone as a complete story
