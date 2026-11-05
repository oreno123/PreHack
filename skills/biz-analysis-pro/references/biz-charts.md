# Business Chart Templates

Quick copy-paste templates for common business analysis figures.

## Setup (always use)

```python
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['figure.dpi'] = 150
matplotlib.rcParams['savefig.dpi'] = 300
plt.style.use('seaborn-v0_8-whitegrid')
```

## 1. Market Size Waterfall (市场规模瀑布图)

```python
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['行业总量', '品类占比', '地域筛选', '渠道筛选', '目标市场']
values = [5700, -4931, -951, -380, -722]  # 正负表示增减
colors = ['#2196F3', '#FF5722', '#FF5722', '#FF5722', '#4CAF50']

cumulative = np.cumsum(values)
starts = [0] + list(cumulative[:-1])

for i, (cat, val, start) in enumerate(zip(categories, values, starts)):
    ax.bar(i, abs(val), bottom=start if val < 0 else start,
           color=colors[i], width=0.6, edgecolor='white', linewidth=1)
    label_y = start + val/2
    ax.text(i, label_y, f'¥{abs(val)}亿', ha='center', va='center',
            fontweight='bold', fontsize=11)

ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)
ax.set_ylabel('市场规模 (亿元)')
ax.set_title('市场规模瀑布分析')
fig.savefig('market_waterfall.png', bbox_inches='tight')
```

## 2. Competitor Positioning Map (竞品定位图)

```python
fig, ax = plt.subplots(figsize=(10, 8))
# X: price level, Y: quality level
companies = ['Company A', 'Company B', 'Company C', 'Company D', 'Our Product']
x = [3, 7, 5, 8, 6]
y = [4, 8, 6, 9, 7]
sizes = [200, 500, 300, 400, 350]
colors = ['#90CAF9', '#90CAF9', '#90CAF9', '#90CAF9', '#FF5722']

ax.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolors='white', linewidth=2)
for i, name in enumerate(companies):
    ax.annotate(name, (x[i], y[i]), textcoords="offset points",
                xytext=(10, 10), fontsize=11)

# Quadrant lines
ax.axhline(y=5.5, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=5.5, color='gray', linestyle='--', alpha=0.5)
ax.text(2.5, 8, '高质低价\n(机会区)', ha='center', fontsize=10, color='green', alpha=0.6)
ax.text(8.5, 8, '高质高价\n(高端区)', ha='center', fontsize=10, color='blue', alpha=0.6)
ax.text(2.5, 3, '低质低价\n(经济区)', ha='center', fontsize=10, color='gray', alpha=0.6)
ax.text(8.5, 3, '低质高价\n(危险区)', ha='center', fontsize=10, color='red', alpha=0.6)

ax.set_xlabel('价格水平 →', fontsize=13)
ax.set_ylabel('品质/体验水平 →', fontsize=13)
ax.set_title('竞品定位图')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
fig.savefig('positioning_map.png', bbox_inches='tight')
```

## 3. Revenue Projection (收入预测图)

```python
fig, ax1 = plt.subplots(figsize=(10, 6))
years = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5']
revenue = [500, 1800, 4200, 8500, 15000]
users = [10, 36, 84, 170, 300]  # 万

color1 = '#2196F3'
color2 = '#FF9800'
ax1.bar(years, revenue, color=color1, alpha=0.7, width=0.5, label='收入(万元)')
ax1.set_ylabel('收入 (万元)', color=color1, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
ax2.plot(years, users, color=color2, marker='o', linewidth=2.5, markersize=8, label='用户数(万)')
ax2.set_ylabel('用户数 (万)', color=color2, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color2)

fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.92))
ax1.set_title('收入与用户增长预测 (5年)')
fig.savefig('revenue_projection.png', bbox_inches='tight')
```

## 4. Funnel Chart (转化漏斗)

```python
fig, ax = plt.subplots(figsize=(8, 6))
stages = ['曝光', '点击', '注册', '付费', '续费']
values = [100000, 15000, 5000, 800, 480]
colors = ['#1565C0', '#1976D2', '#1E88E5', '#42A5F5', '#64B5F6']

widths = [v/max(values) for v in values]
for i, (stage, val, w) in enumerate(zip(stages, values, widths)):
    ax.barh(len(stages)-1-i, w*10, height=0.7, left=(10-w*10)/2,
            color=colors[i], edgecolor='white', linewidth=2)
    ax.text(5, len(stages)-1-i, f'{stage}\n{val:,} ({val/values[0]*100:.1f}%)',
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')

ax.set_xlim(0, 10)
ax.set_ylim(-0.5, len(stages)-0.5)
ax.axis('off')
ax.set_title('用户转化漏斗', fontsize=14, pad=20)
fig.savefig('funnel.png', bbox_inches='tight')
```

## 5. Risk Matrix (风险矩阵)

```python
fig, ax = plt.subplots(figsize=(8, 8))
risks = {
    '市场需求不及预期': (3.5, 7),
    '竞争对手快速跟进': (6, 5),
    '政策监管收紧': (4, 8),
    '获客成本上升': (7, 6),
    '技术路线失败': (2, 9),
    '人才流失': (5, 4),
}

colors_risk = []
for (x, y) in risks.values():
    score = x * y
    if score > 40: colors_risk.append('#F44336')
    elif score > 20: colors_risk.append('#FF9800')
    else: colors_risk.append('#4CAF50')

x_vals = [v[0] for v in risks.values()]
y_vals = [v[1] for v in risks.values()]
ax.scatter(x_vals, y_vals, s=300, c=colors_risk, alpha=0.8, edgecolors='white', linewidth=2)

for name, (x, y) in risks.items():
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(12, 8), fontsize=10)

ax.set_xlabel('发生概率 →', fontsize=13)
ax.set_ylabel('影响程度 →', fontsize=13)
ax.set_title('风险评估矩阵')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axhline(y=5, color='gray', linestyle='--', alpha=0.3)
ax.axvline(x=5, color='gray', linestyle='--', alpha=0.3)
fig.savefig('risk_matrix.png', bbox_inches='tight')
```

## 6. Porter's Five Forces Diagram (波特五力图)

```python
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Center
ax.add_patch(plt.Rectangle((3.5, 3.5), 3, 3, fill=True, facecolor='#E3F2FD',
                             edgecolor='#1565C0', linewidth=2))
ax.text(5, 5, '行业竞争\n强度: 高', ha='center', va='center', fontsize=12, fontweight='bold')

# Four surrounding forces
forces = {
    'new': (5, 8.5, '新进入者威胁\n壁垒: 中'),
    'sub': (5, 1.5, '替代品威胁\n程度: 低'),
    'supplier': (1.5, 5, '供应商议价\n能力: 中'),
    'buyer': (8.5, 5, '买方议价\n能力: 高'),
}
colors_f = {'new': '#FFF3E0', 'sub': '#E8F5E9', 'supplier': '#F3E5F5', 'buyer': '#FFEBEE'}
for key, (x, y, text) in forces.items():
    ax.add_patch(plt.Rectangle((x-1.2, y-0.8), 2.4, 1.6, fill=True,
                                facecolor=colors_f[key], edgecolor='gray', linewidth=1.5))
    ax.text(x, y, text, ha='center', va='center', fontsize=10)

# Arrows
for (x, y) in [(5, 7.7), (5, 2.3), (2.7, 5), (7.3, 5)]:
    ax.annotate('', xy=(5, 5), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

ax.axis('off')
ax.set_title("波特五力分析", fontsize=14, fontweight='bold')
fig.savefig('porter_five_forces.png', bbox_inches='tight')
```

## 7. Business Model Canvas Visualization

```python
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)

blocks = [
    (0, 5, 3, 5, 'Key Partners\n\n• 合作伙伴1\n• 合作伙伴2'),
    (0, 3, 3, 2, 'Key Activities\n\n• 核心活动1\n• 核心活动2'),
    (0, 0, 3, 3, 'Key Resources\n\n• 核心资源1\n• 核心资源2'),
    (3, 5, 3, 5, 'Value Proposition\n\n• 核心价值1\n• 核心价值2\n• 核心价值3'),
    (6, 7, 3, 3, 'Customer\nRelationships\n\n• 关系类型1'),
    (6, 4, 3, 3, 'Channels\n\n• 渠道1\n• 渠道2'),
    (9, 5, 3.5, 5, 'Customer\nSegments\n\n• 用户群1\n• 用户群2'),
    (6, 0, 6.5, 4, 'Revenue Streams\n\n• 收入来源1\n• 收入来源2'),
    (0, 0, 12.5, 10, ''),  # outer frame handled by blocks
]

colors_b = ['#E3F2FD', '#FFF3E0', '#E8F5E9', '#FFFDE7',
            '#F3E5F5', '#E0F7FA', '#FFEBEE', '#F1F8E9']

for i, (x, y, w, h, text) in enumerate(blocks[:8]):
    ax.add_patch(plt.Rectangle((x, y), w, h, fill=True,
                                facecolor=colors_b[i], edgecolor='#424242', linewidth=1.5))
    ax.text(x + w/2, y + h - 0.5, text, ha='center', va='top', fontsize=9,
            linespacing=1.5)

# Cost structure
ax.add_patch(plt.Rectangle((12.5, 0), 3.5, 10, fill=True,
                             facecolor='#FAFAFA', edgecolor='#424242', linewidth=1.5))
ax.text(14.25, 5, 'Cost Structure\n\n• 成本项1\n• 成本项2\n• 成本项3',
        ha='center', va='center', fontsize=9, linespacing=1.5)

ax.axis('off')
ax.set_title('商业模式画布', fontsize=16, fontweight='bold', pad=15)
fig.savefig('business_model_canvas.png', bbox_inches='tight')
```

## Save Checklist
- [ ] `bbox_inches='tight'` on all saves
- [ ] Save both PNG and PDF
- [ ] DPI >= 300
- [ ] Font >= 12
- [ ] Colorblind-friendly
- [ ] Figure referenced in text before appearing
