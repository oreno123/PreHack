# 卡 · 九大题型与出题趋势

> 来源：自维护竞赛指南（CUMCM 2020-2025 获奖论文归纳）。选题快评时按题型对号入座。

## 九大题型速览

| 题型 | 核心方法 | 求解器/工具 |
|---|---|---|
| 优化类（国赛必考最高频） | LP/IP/MILP/NLP/多目标/DP/启发式(GA·SA·PSO·ACO) | PuLP, Gurobi, `intlinprog`, `fmincon` |
| 预测类 | ARIMA·SARIMA·Prophet·灰色GM(1,1)·XGBoost·LSTM·马尔可夫 | statsmodels, Prophet |
| 评价类 | **三件套**：AHP(主观)+熵权法(客观)+TOPSIS(排序)；模糊综合/PCA/灰色关联 | 手写为主 |
| 分类/聚类 | 有标签：小数据 SVM/RF，大 XGBoost；无标签：知 k 用 K-Means/GMM，不知用 DBSCAN | sklearn |
| 图论/网络 | Dijkstra/Floyd、TSP 用 GA/LKH、网络流、PageRank/中心性、社区发现 | networkx |
| 微分方程 | SIR/SEIR、RK4 数值解、PDE 差分；物理机理题=守恒律建 ODE+数值求解+参数优化 | scipy.integrate |
| 排班调度 | MIP+Gurobi（精确）、GA/PSO（近似）、甘特图 | Gurobi |
| 随机统计 | 蒙特卡洛、排队论 M/M/c、马尔可夫链、Bootstrap | numpy/simpy |
| 混合题型 | 三层结构：基础模型(30%)→改进模型(50%)→扩展模型(20%) | — |

**混合建模是主流**：近年 O 奖约 83% 用混合模型，单一模型论文越来越难拿高档。

## 分类算法选择树

```
有标签？
├─ 是 → 数据量？小→SVM/RF/KNN，大→XGBoost/NN
└─ 否 → 知道类别数？是→K-Means/GMM，否→DBSCAN/层次聚类
```

## 2020-2025 出题趋势

| 方向 | 代表赛题 | 说明 |
|---|---|---|
| AI/ML 融合 | 2023 国赛 C 蔬菜定价、2024 美赛 C | XGBoost/LSTM 成标配，但需与传统方法对比 |
| 鲁棒优化 | 2024 国赛 B、2024 美赛 E | 处理参数不确定性成加分项 |
| GIS/空间分析 | 2024 美赛 E（MGWR） | 地理加权回归越来越常见 |
| 双碳/可持续 | 2024 美赛 E、2025 国赛 B | 环境科学+政策类题目增多 |
| 博弈论 | 2020 国赛 B 穿越沙漠 | 动态博弈在多人决策题中高频 |
