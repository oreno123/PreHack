# 卡 · 12 个获奖样本的可复用套路链

> 来源：2020-2025 国赛/美赛获奖论文归纳。外部标杆，非亲历——打完比赛回填亲历卡覆盖本卡。

## 套路链速查

| # | 赛题 | 核心方法链 | 可复用套路 |
|---|---|---|---|
| 1 | 2024 美赛 E（O 奖） | MGWR+熵权法+系统动力学+蒙特卡洛 | 评价+系统动力学+蒙特卡洛（**O 套路**） |
| 2 | 2024 国赛 C | MILP+鲁棒优化+蒙特卡洛 | 规划+鲁棒优化 |
| 3 | 2024 国赛 A | ODE+空间几何+GA 优化 | 几何+ODE+优化 |
| 4 | 2023 国赛 A（国一） | 光学物理+数值积分+三分查找 | 机理建模+启发式优化 |
| 5 | 2023 国赛 C（国一） | ARIMA+Prophet+模拟退火 | 预测+启发式优化 |
| 6 | 2022 国赛 C | PCA+K-Means+SVM/RF | 统计→聚类→分类 |
| 7 | 2021 国赛 C | AHP+熵权法+整数规划+网络优化 | 评价筛选→优化分配 |
| 8 | 2020 国赛 B | DP+马尔可夫+蒙特卡洛+博弈论 | 图论+DP+随机过程 |
| 9 | 2020 国赛 A | PDE 热传导+差分法+参数优化 | PDE+数值求解+优化 |
| 10 | 2022 美赛 E | ODE+多目标优化+Pareto | ODE+多目标+蒙特卡洛 |
| 11 | 2024 美赛 C | 多源数据+ARIMA+XGBoost+分位数回归 | 多源融合+混合预测 |
| 12 | 2021 美赛 D（O 奖） | SNA+PageRank+PCA+K-Means | PageRank+网络中心性跨界 |

## 高频组合拳

- **供应链题万能链**：评价(AHP/TOPSIS 选供应商) → 整数规划(定订购量) → 网络优化(定路线)
- **预测双保险**：ARIMA + Prophet/XGBoost 双模型 + 残差分析 + 预测区间
- **评价三件套**：AHP + 熵权法组合赋权 → TOPSIS 排序
- **物理机理题**：守恒律建 ODE → RK4 数值解 → 参数优化(fmincon/三分/GA)
- **统计文物类**（2022 玻璃）：PCA 降维 → K-Means 聚类 → SVM/RF 分类 → 卡方/t 检验

## 资源

- 官方：[国赛官网](https://www.mcm.edu.cn) | [美赛官网](https://www.comap.com) | [教育部获奖论文](https://dxs.moe.gov.cn/zx/hd/sxjm/sxjmlw/)
- 学习：[数模知识库](https://www.shumo.com/wiki/) | [MathModelHub](https://github.com/Jaxon1216/MathModelHub) | [MCM/ICM O 奖存档](https://sourceforge.net/projects/mcm-icm.mirror/)
- 开源获奖论文：[2024 美赛 E O 奖](https://github.com/ydchen-chen0806/24ICM_E_O_Award_Paper_code) | [2021 美赛 D O 奖](https://github.com/liujiyaoFDU/2021-ICM-D-Outstanding) | [2023 国赛 A 国一](https://github.com/linggm3/2023_CUMCM_National-First-Prize) | [2020B 穿越沙漠](https://github.com/seanys/CUMCM2020-Desert-Game) | [优秀论文合集](https://github.com/zhanwen/MathModel)
