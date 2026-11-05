# Visualization Guide for Math Modeling Papers

Quick reference for generating publication-quality figures.

## Matplotlib Setup (always use this preamble)

```python
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Preamble — copy to every visualization script
matplotlib.rcParams['font.family'] = 'SimHei'  # Chinese font
matplotlib.rcParams['axes.unicode_minus'] = False  # Fix minus sign
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['figure.dpi'] = 150  # Screen; save at 300 DPI
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['figure.figsize'] = (8, 5)

plt.style.use('seaborn-v0_8-whitegrid')  # Clean grid style
```

## Common Figure Types

### 1. Convergence Curve (优化收敛)
```python
fig, ax = plt.subplots()
ax.plot(iterations, best_values, linewidth=2, color='#2196F3')
ax.set_xlabel('Iteration')
ax.set_ylabel('Objective Function Value')
ax.set_title('Convergence Curve')
fig.savefig('convergence.png', bbox_inches='tight')
fig.savefig('convergence.pdf', bbox_inches='tight')
```

### 2. Heatmap (相关性/参数扫描)
```python
import seaborn as sns
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(data, annot=True, fmt='.2f', cmap='YlOrRd',
            xticklabels=x_labels, yticklabels=y_labels, ax=ax)
ax.set_title('Parameter Sensitivity Heatmap')
fig.savefig('heatmap.png', bbox_inches='tight')
```

### 3. Comparison Bar Chart (方法对比)
```python
fig, ax = plt.subplots()
x = np.arange(len(methods))
width = 0.25
ax.bar(x - width, metric_a, width, label='Metric A', color='#4CAF50')
ax.bar(x, metric_b, width, label='Metric B', color='#2196F3')
ax.bar(x + width, metric_c, width, label='Metric C', color='#FF9800')
ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.legend()
ax.set_ylabel('Score')
ax.set_title('Method Comparison')
fig.savefig('comparison.png', bbox_inches='tight')
```

### 4. Scatter + Regression (散点+回归)
```python
fig, ax = plt.subplots()
ax.scatter(x_data, y_data, alpha=0.6, s=30, color='#2196F3', label='Data')
z = np.polyfit(x_data, y_data, 1)
p = np.poly1d(z)
x_line = np.linspace(x_data.min(), x_data.max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'Fit: y={z[0]:.3f}x+{z[1]:.3f}')
ax.legend()
ax.set_xlabel('X Variable')
ax.set_ylabel('Y Variable')
fig.savefig('scatter_fit.png', bbox_inches='tight')
```

### 5. Cluster Visualization (聚类)
```python
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=42)
embedded = tsne.fit_transform(high_dim_data)
fig, ax = plt.subplots()
scatter = ax.scatter(embedded[:, 0], embedded[:, 1], c=labels, cmap='Set2', s=30, alpha=0.7)
ax.legend(*scatter.legend_elements(), title='Cluster')
ax.set_title('Cluster Visualization (t-SNE)')
fig.savefig('cluster.png', bbox_inches='tight')
```

### 6. Sensitivity Tornado (灵敏度龙卷风图)
```python
fig, ax = plt.subplots()
params = ['α', 'β', 'γ', 'δ']
low_impact = [-5, -3, -8, -2]
high_impact = [6, 4, 7, 3]
y_pos = np.arange(len(params))
ax.barh(y_pos, high_impact, align='center', height=0.4, color='#4CAF50', label='+10%')
ax.barh(y_pos, low_impact, align='center', height=0.4, color='#F44336', label='-10%')
ax.set_yticks(y_pos)
ax.set_yticklabels(params)
ax.set_xlabel('Change in Output (%)')
ax.set_title('Sensitivity Analysis')
ax.legend()
ax.axvline(x=0, color='black', linewidth=0.5)
fig.savefig('sensitivity_tornado.png', bbox_inches='tight')
```

### 7. 3D Surface (三维曲面)
```python
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
X, Y = np.meshgrid(x_range, y_range)
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Objective Function Surface')
fig.colorbar(surf, shrink=0.5, aspect=5)
fig.savefig('surface3d.png', bbox_inches='tight')
```

### 8. Time Series Forecast (时序预测)
```python
fig, ax = plt.subplots()
ax.plot(dates, actual, linewidth=1.5, color='#2196F3', label='Actual')
ax.plot(dates, predicted, linewidth=1.5, color='#F44336', linestyle='--', label='Predicted')
ax.fill_between(dates, lower_bound, upper_bound, alpha=0.2, color='#F44336', label='95% CI')
ax.legend()
ax.set_xlabel('Date')
ax.set_ylabel('Value')
ax.set_title('Time Series Forecast')
fig.savefig('forecast.png', bbox_inches='tight')
```

### 9. Network Graph (网络图)
```python
import networkx as nx
fig, ax = plt.subplots(figsize=(10, 8))
G = nx.Graph()
G.add_edges_from(edges)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=500, font_size=10, ax=ax)
ax.set_title('Network Topology')
fig.savefig('network.png', bbox_inches='tight')
```

### 10. Correlation Matrix (相关系数矩阵)
```python
fig, ax = plt.subplots(figsize=(10, 8))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, square=True, ax=ax)
ax.set_title('Feature Correlation Matrix')
fig.savefig('correlation.png', bbox_inches='tight')
```

## Color Palettes

Always use colorblind-friendly palettes:

```python
# Categorical (up to 8 categories)
colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0', '#00BCD4', '#795548', '#607D8B']

# Sequential
cmap = 'YlOrRd'  # Yellow-Orange-Red
cmap = 'Blues'    # Blue shades
cmap = 'viridis'  # Perceptually uniform

# Diverging
cmap = 'RdBu_r'  # Red-Blue (centered at 0)
cmap = 'RdYlGn'  # Red-Yellow-Green
```

## Save Checklist
- [ ] `bbox_inches='tight'` on all saves (no clipping)
- [ ] Save both PNG (raster) and PDF (vector)
- [ ] DPI >= 300
- [ ] Font size >= 12
- [ ] All axes labeled with units
- [ ] Legend present if multiple series
- [ ] No overlapping text
