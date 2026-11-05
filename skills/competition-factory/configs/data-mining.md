# Data Mining Competition Config (Kaggle/天池/和鲸)

## Roles

| Role | Responsibility |
|------|---------------|
| **Data Engineer** | 数据加载、清洗、特征工程 |
| **Explorer** | EDA、分布分析、异常检测 |
| **Feature Engineer** | 特征构造、特征选择、降维 |
| **Modeler** | 模型训练、调参、融合 |
| **Validator** | 交叉验证、过拟合检测、消融实验 |
| **Reporter** | 技术报告撰写 |

## Pipeline

```
1. Competition Intake → 读懂赛题、评价指标、数据说明、提交格式
2. EDA                → 数据分布、缺失值、异常值、标签分布、特征相关性
3. Baseline           → 快速跑通一个简单模型，建立benchmark
4. Feature Engineering→ 构造有效特征、特征选择
5. Model Selection    → 对比多个模型（LightGBM/XGBoost/NN）
6. Hyperparameter Tuning → Optuna/GridSearch
7. Model Ensemble     → Stacking/Blending/Weighted Average
8. Validation         → 交叉验证、过拟合检测、 Leakage检查
9. Submission         → 生成提交文件、检查格式
10. Technical Report  → 写技术报告（方法论、实验、结果）
```

## Output Format

### 技术报告结构
```
一、赛题理解
├── 问题描述
├── 评价指标
└── 数据概况

二、探索性数据分析
├── 数据分布
├── 特征相关性
├── 异常值检测
└── 关键发现

三、特征工程
├── 特征构造（列出所有新特征及思路）
├── 特征选择方法
└── 最终特征集

四、模型方案
├── 基线模型
├── 模型对比实验
├── 最终模型架构
└── 超参数设置

五、模型融合
├── 融合策略
├── 各单模型表现
└── 融合后提升

六、实验结果
├── 交叉验证分数
├── 线上分数
├── 消融实验
└── 关键发现

七、总结与改进方向
```

## Key Libraries
```python
# Standard stack
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, f1_score, roc_auc_score
import lightgbm as lgb
import xgboost as xgb
from optuna import create_study
```

## Actor-Critic Rules
- **EDA**: 1 round (completeness)
- **Feature Engineering**: 2 rounds (effectiveness check)
- **Model**: 2 rounds (overfitting check)
- **Final Report**: 1 round

## Critical Rules
- **No data leakage**: Never use future data or test data in training
- **Stratified CV**: Always stratify for classification, time-series split for forecasting
- **Reproducibility**: Fix seeds, save models, version features
- **Overfitting watch**: If CV score >> LB score, something is wrong
- **Metric alignment**: Optimize for the exact competition metric, not proxy metrics
