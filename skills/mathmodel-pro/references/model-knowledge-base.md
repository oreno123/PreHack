# Model Knowledge Base (HMML-inspired)

Hierarchical model selection guide. Three levels: **Domain → Subdomain → Method**.

## 1. Optimization (优化)

### 1.1 Linear Optimization
| Method | When to use | Python | Key libraries |
|--------|-------------|--------|---------------|
| LP (单纯形法) | Linear objective + linear constraints | `scipy.optimize.linprog` or `pulp` | `scipy`, `pulp`, `cvxpy` |
| Integer LP | Variables must be integers | `pulp` or `gurobipy` | `pulp`, `cvxpy` |
| Transportation Problem | Supply-demand matching | `pulp` | `pulp` |

### 1.2 Nonlinear Optimization
| Method | When to use | Python |
|--------|-------------|--------|
| Gradient descent | Smooth differentiable functions | `scipy.optimize.minimize` |
| Genetic Algorithm (GA) | Non-convex, discrete search space | `scikit-opt (sko)`, `DEAP` |
| Simulated Annealing (SA) | Combinatorial optimization | `scipy.optimize.dual_annealing`, `sko.SA` |
| Particle Swarm (PSO) | Multi-modal continuous optimization | `sko.PSO`, `pyswarm` |
| Differential Evolution | Global optimization, robust | `scipy.optimize.differential_evolution` |

### 1.3 Multi-objective Optimization
| Method | When to use | Python |
|--------|-------------|--------|
| Weighted sum | Convert to single objective | `scipy.optimize` |
| NSGA-II | Pareto front needed | `pymoo.algorithms.nsga2` |
| TOPSIS | Decision-making from alternatives | Custom implementation |
| Entropy weight | Objective weighting method | `scipy.stats.entropy` |

## 2. Statistical Analysis (统计分析)

### 2.1 Regression
| Method | When to use | Python |
|--------|-------------|--------|
| OLS Linear regression | Linear relationship, interpretation | `statsmodels.OLS`, `sklearn.LinearRegression` |
| Ridge/Lasso | Multicollinearity, feature selection | `sklearn.Ridge/Lasso` |
| Polynomial regression | Nonlinear but smooth | `sklearn.PolynomialFeatures` + `LinearRegression` |
| Logistic regression | Binary/multiclass classification | `sklearn.LogisticRegression` |

### 2.2 Hypothesis Testing
| Test | When to use | Python |
|------|-------------|--------|
| t-test | Compare two group means | `scipy.stats.ttest_ind` |
| ANOVA | Compare 3+ group means | `scipy.stats.f_oneway` |
| Chi-square | Categorical variable association | `scipy.stats.chi2_contingency` |
| KS test | Distribution comparison | `scipy.stats.ks_2samp` |
| Normality test | Check normal assumption | `scipy.stats.shapiro` |

### 2.3 Time Series
| Method | When to use | Python |
|--------|-------------|--------|
| ARIMA | Univariate time series forecast | `statsmodels.ARIMA` |
| Exponential Smoothing | Short-term forecast with trend/seasonality | `statsmodels.ExponentialSmoothing` |
| Prophet | Multiple seasonalities, holidays | `prophet` |
| LSTM | Complex nonlinear patterns | `torch` or `tf.keras` |
| VAR | Multivariate time series | `statsmodels.VAR` |

## 3. Machine Learning (机器学习)

### 3.1 Supervised
| Method | When to use | Python |
|--------|-------------|--------|
| Random Forest | Robust baseline, feature importance | `sklearn.RandomForestClassifier/Regressor` |
| XGBoost/LightGBM | Best tabular performance | `xgboost`, `lightgbm` |
| SVM | Small sample, high-dim, clear margin | `sklearn.SVC/SVR` |
| KNN | Simple, distance-based | `sklearn.KNeighborsClassifier` |

### 3.2 Unsupervised
| Method | When to use | Python |
|--------|-------------|--------|
| KMeans | Spherical clusters, known K | `sklearn.KMeans` |
| DBSCAN | Arbitrary shape clusters, noise | `sklearn.DBSCAN` |
| GMM | Soft clustering, elliptical clusters | `sklearn.GaussianMixture` |
| Hierarchical clustering | Dendrogram needed, small dataset | `scipy.cluster.hierarchy` |
| PCA | Dimensionality reduction, visualization | `sklearn.PCA` |

### 3.3 Deep Learning
| Method | When to use | Python |
|--------|-------------|--------|
| CNN | Image data | `torch.nn.Conv2d` |
| RNN/LSTM | Sequence data | `torch.nn.LSTM` |
| GNN | Graph-structured data | `torch_geometric` |

## 4. Differential Equations (微分方程)

### 4.1 ODE
| Method | When to use | Python |
|--------|-------------|--------|
| `solve_ivp` (RK45) | Standard ODE systems | `scipy.integrate.solve_ivp` |
| Euler method | Simple, educational | Custom loop |
| Stiff solver | Stiff systems | `scipy.integrate.solve_ivp(method='Radau')` |

### 4.2 PDE
| Method | When to use | Python |
|--------|-------------|--------|
| Finite difference | Regular grids | `scipy` + custom implementation |
| Finite element | Complex geometries | `fenics`, `pygmsh` |

### 4.3 Common Competition Models
| Model | Application | Key equations |
|-------|-------------|---------------|
| SIR/SEIR | Epidemic spread | dS/dt, dI/dt, dR/dt |
| Lotka-Volterra | Predator-prey dynamics | dx/dt, dy/dt |
| Logistic growth | Population with carrying capacity | dN/dt = rN(1-N/K) |
| Heat equation | Heat diffusion | du/dt = α∇²u |

## 5. Graph & Network (图论与网络)

| Method | When to use | Python |
|--------|-------------|--------|
| Shortest path (Dijkstra) | Route optimization | `networkx.shortest_path` |
| MST (Kruskal/Prim) | Minimum cost spanning | `networkx.minimum_spanning_tree` |
| Max flow | Resource allocation | `networkx.maximum_flow` |
| PageRank | Node importance | `networkx.pagerank` |
| Community detection | Cluster in networks | `networkx.community` |
| TSP | Travel route optimization | `networkx.approximation.traveling_salesman_problem` |
| VRP | Vehicle routing | `ortools` |

## 6. Evaluation & Decision (评价与决策)

| Method | When to use | Python |
|--------|-------------|--------|
| AHP | Hierarchical decision-making | Custom (`numpy.linalg.eig`) |
| TOPSIS | Multi-criteria ranking | Custom |
| Entropy weight | Objective weighting | `scipy.stats.entropy` |
| Grey relational | Small sample, uncertain info | Custom |
| Fuzzy comprehensive | Fuzzy criteria evaluation | `skfuzzy` |
| PCA + scoring | Comprehensive evaluation | `sklearn.PCA` |

## 7. Interpolation & Fitting (插值与拟合)

| Method | When to use | Python |
|--------|-------------|--------|
| Spline interpolation | Smooth curve through data points | `scipy.interpolate.CubicSpline` |
| B-spline | More control over smoothness | `scipy.interpolate.BSpline` |
| Least squares fit | Fit a specific function form | `scipy.optimize.curve_fit` |
| RBF interpolation | Scattered multi-dimensional data | `scipy.interpolate.RBFInterpolator` |

## 8. Model Selection Decision Tree

```
问题类型?
├── 预测/预报
│   ├── 连续值 → 回归 (§2.1)
│   ├── 类别 → 分类 (§3.1)
│   └── 时间 → 时间序列 (§2.3)
├── 优化/决策
│   ├── 线性 → LP (§1.1)
│   ├── 非线性 → GA/SA/PSO (§1.2)
│   └── 多目标 → NSGA-II/TOPSIS (§1.3)
├── 分类/聚类
│   ├── 有标签 → 监督学习 (§3.1)
│   └── 无标签 → 聚类 (§3.2)
├── 评价/排序
│   └── 综合 → AHP/TOPSIS/熵权 (§6)
├── 过程模拟
│   ├── 连续 → 微分方程 (§4)
│   └── 离散 → 仿真/元胞自动机
└── 网络/路径
    └── 图论 (§5)
```
