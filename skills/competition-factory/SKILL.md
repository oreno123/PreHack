---
name: competition-factory
description: Use when entering any academic competition — mathematical modeling (CUMCM/MCM/ICM), business analysis, innovation & entrepreneurship (互联网+/挑战杯), case competitions, data mining competitions (Kaggle/天池). Auto-detects competition type and dispatches the right specialist workflow. Trigger words: 比赛、竞赛、商赛、商业分析、创新创业、案例大赛、数据挖掘竞赛、competition、hackathon、case competition、business plan、startup competition.
---

# Competition Factory — Universal Competition Skill

Auto-detect competition type from problem description, then dispatch the correct specialist workflow with appropriate roles, pipeline, templates, and domain knowledge.

## Step 0: Detect Competition Type

Read the problem file or user description. Match against these signals:

| Signals in problem | Type | Key |
|--------------------|------|-----|
| 建立数学模型、求解、优化、微分方程、蒙特卡洛 | **数学建模** | `math-modeling` |
| 赛题有明确子问题 (问题一/二/三, Task 1/2/3) + 数据文件 | **数学建模** | `math-modeling` |
| market analysis, industry research, 竞品分析, 商业模式, ROI | **商业分析** | `biz-analysis` |
| 商业计划书, 路演, 创业, 商业模式画布, 融资 | **创新创业** | `innovation` |
| 案例分析, 企业诊断, 战略建议, 咨询报告 | **案例大赛** | `case-study` |
| leaderboard, submit, train/test split, 评价指标, AUC/F1/RMSE | **数据挖掘竞赛** | `data-mining` |

If ambiguous, **ask the user** which type. Do not guess wrong.

## Step 1: Load Competition Config

Once type is detected, read the corresponding config file:

| Type | Config | Also loads |
|------|--------|------------|
| `math-modeling` | `configs/math-modeling.md` | mathmodel-pro skill |
| `biz-analysis` | `configs/biz-analysis.md` | — |
| `innovation` | `configs/innovation.md` | — |
| `case-study` | `configs/case-study.md` | — |
| `data-mining` | `configs/data-mining.md` | — |

<HARD-GATE>
Read the config file BEFORE dispatching any subagent. The config defines roles, pipeline stages, and output format specific to this competition type.
</HARD-GATE>

## Step 2: Initialize Workspace

```bash
mkdir -p work_dir/{raw_data,processed,scripts,results,figures,paper}
```

Save detected competition type and config to `work_dir/competition_meta.json`:
```json
{
  "type": "biz-analysis",
  "name": "2024全国大学生商业分析大赛",
  "subtasks": 3,
  "data_files": ["market_data.csv"],
  "deadline": "2024-05-01",
  "team_info": {}
}
```

## Step 3: Execute Competition-Specific Pipeline

Follow the pipeline defined in the loaded config. Each config specifies:

1. **Roles** — which subagents to dispatch
2. **Pipeline** — ordered stages with dependencies
3. **Actor-Critic** — how many review rounds per stage
4. **Output format** — paper, report, slides, or code submission
5. **Domain references** — which reference files to consult

## Universal Principles (apply to ALL types)

### Actor-Critic at Every Stage
Every major output goes through: Generate → Review → Improve (minimum 2 rounds). Never accept first draft.

### No Fabricated Results
If code fails, data is missing, or analysis is inconclusive — report honestly. Do not fabricate numbers, chart data, or conclusions.

### Deterministic Reproducibility
- All code sets random seeds
- All data processing is scripted (no manual Excel)
- All figures saved as code, not screenshots

### Parallel When Possible
Independent subtasks or pipeline stages should be dispatched as parallel subagents using multiple Agent tool calls in one message.

### Evidence-Based Claims
Every claim in the final output must be backed by: data analysis, model output, cited reference, or clearly stated assumption. No unsupported assertions.

## Quick Config Summary

### Math Modeling (`math-modeling`)
- **Roles**: Analyst, Modeler, Coder, Artist, Writer, Reviewer
- **Pipeline**: Problem Intake → Analysis → Decompose (DAG) → Model Select → Data Clean → Code → Visualize → Paper → Review
- **Output**: Academic paper (Markdown + LaTeX)
- **Full config**: see `configs/math-modeling.md` or use mathmodel-pro skill directly

### Business Analysis (`biz-analysis`)
- **Roles**: Industry Researcher, Data Analyst, Strategist, Financial Modeler, Report Writer, Reviewer
- **Pipeline**: Industry Scan → Problem Frame → Data Collection → Market Analysis → Strategy Design → Financial Model → Risk Analysis → Report → Slides
- **Output**: Business analysis report + presentation slides
- **Key frameworks**: Porter's 5 Forces, PESTEL, SWOT, Business Model Canvas, AARRR, TAM/SAM/SOM

### Innovation & Entrepreneurship (`innovation`)
- **Roles**: Market Researcher, Product Designer, Business Planner, Financial Modeler, Pitch Writer, Reviewer
- **Pipeline**: Problem Identify → Market Validation → Solution Design → Business Model → Go-to-Market → Financial Projection → Risk Analysis → Business Plan → Pitch Deck
- **Output**: Business plan document + pitch deck (PPT)
- **Key frameworks**: Lean Canvas, Jobs-to-be-Done, Blue Ocean Strategy, Unit Economics

### Case Study (`case-study`)
- **Roles**: Industry Analyst, Problem Diagnostician, Solution Architect, Implementation Planner, Report Writer, Reviewer
- **Pipeline**: Case Intake → Company/Industry Research → Problem Diagnosis → Root Cause Analysis → Solution Design → Implementation Plan → Risk Mitigation → Report
- **Output**: Consulting-style report (structured like McKinsey/BCG deliverable)
- **Key frameworks**: MECE, Issue Tree, 7S Model, Value Chain, BCG Matrix

### Data Mining (`data-mining`)
- **Roles**: Data Engineer, Feature Engineer, Modeler, Validator, Report Writer
- **Pipeline**: Data Intake → EDA → Feature Engineering → Baseline Model → Model Tuning → Ensemble → Validation → Submission → Report
- **Output**: Prediction submission file + technical report
- **Key tools**: pandas, sklearn, xgboost, lightgbm, torch

## Extending with New Competition Types

To add a new competition type:

1. Create `configs/new-type.md` following this template:
```markdown
# [Competition Type Name] Config

## Roles
| Role | Responsibility |
|------|---------------|
| ... | ... |

## Pipeline
1. Stage 1 — ...
2. Stage 2 — ...

## Output Format
...

## Domain References
- `references/xxx.md`
```

2. Add detection signals to Step 0 above
3. Add entry to the Quick Config Summary table
4. Create any needed reference files in `references/`

## Integration with Other Skills

- **mathmodel-pro**: For `math-modeling` type, this skill delegates to the dedicated mathmodel-pro skill
- **huashu-md-html**: Convert final reports to styled HTML or DOCX
- **guizang-ppt-skill**: Generate presentation slides for biz-analysis or innovation types
- **data-cleaning-and-visualization**: If installed, use for data processing stage
