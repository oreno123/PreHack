# Paper Structure Template

Standard structure for CUMCM/MCM/ICM papers. Adjust section titles based on competition type.

## Chinese Competition (国赛 CUMCM) Template

```
标题（20字以内，点明方法和问题）

摘要（一页，最重要部分）
├── 问题背景（1-2句）
├── 针对问题一：方法 + 关键结果（数据）
├── 针对问题二：方法 + 关键结果（数据）
├── 针对问题三：方法 + 关键结果（数据）
├── 模型特色/创新点（1-2句）
└── 关键词（3-5个）

一、问题重述
├── 1.1 问题背景
└── 1.2 问题提出（列出所有子问题）

二、模型假设与符号说明
├── 2.1 模型假设（编号列出，每条说明理由）
└── 2.2 符号说明（三线表：符号 | 含义 | 单位）

三、问题一的分析与建模
├── 3.1 问题分析
├── 3.2 模型建立
│   ├── 变量定义
│   ├── 目标函数/约束条件
│   └── 数学公式（编号）
├── 3.3 模型求解
│   ├── 算法描述（伪代码或流程图）
│   ├── 求解过程
│   └── 计算结果
└── 3.4 结果分析
    ├── 结果展示（表格+图）
    └── 结果讨论

四、问题二的分析与建模（同上结构）
五、问题三的分析与建模（同上结构）

六、模型评价与推广
├── 6.1 模型优点
├── 6.2 模型缺点
└── 6.3 模型推广（如何应用到更一般情况）

七、参考文献
附录（代码）
```

## American Competition (美赛 MCM/ICM) Template

```
Title (descriptive, not cute)

Summary Sheet (one page)
├── Restate problem briefly
├── Method for each subtask with key results
├── Conclusions and recommendations
├── Strengths of approach
└── Keywords

1. Introduction
├── 1.1 Problem Background
├── 1.2 Problem Restatement
└── 1.3 Our Approach (overview of methodology)

2. Assumptions and Justifications
├── Listed assumptions with justification for each
└── Table of Notation

3. [Model Name] for Task 1
├── 3.1 Model Design
│   ├── Variables and parameters
│   ├── Mathematical formulation
│   └── Justification of model choice
├── 3.2 Solution Method
│   ├── Algorithm (pseudocode)
│   └── Implementation details
└── 3.3 Results and Analysis
    ├── Tables and figures
    └── Discussion of results

4. [Model Name] for Task 2 (same structure)
5. [Model Name] for Task 3 (same structure)

6. Sensitivity Analysis
├── Parameter perturbation tests
├── Robustness analysis
└── Impact on conclusions

7. Model Evaluation
├── 7.1 Strengths
├── 7.2 Weaknesses
└── 7.3 Future Improvements

8. Conclusion

References
Appendix: Code
```

## Writing Guidelines

### Abstract Rules
- **Most important section** — judges read this first
- One page maximum
- Include **specific numbers**: "accuracy reached 95.3%", "reduced cost by 23.1%"
- Name the specific model/algorithm used for each subtask
- End with 1-2 sentences on model innovation

### Mathematical Notation
- Display equations: `$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$` (numbered)
- Inline: `$x_i$ denotes the $i$-th variable`
- All variables defined in notation table before first use
- Equations numbered sequentially: (1), (2), (3)...

### Tables
- Use 三线表 (three-line table style)
- Header bold, no vertical lines
- Caption above table
- All columns have units

### Figures
- Caption below figure
- DPI >= 300
- Font size >= 12 for axis labels
- Colorblind-friendly palette
- Referenced in text before appearing: "如图1所示"

### Code Appendix
- Clean, commented Python code
- Remove debugging print statements
- Include only core algorithm, not boilerplate
- Organized by subtask: `q1_model.py`, `q2_model.py`
