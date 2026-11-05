---
name: data-map-pptx
description: "Generate editable China province scoring map PPTX from a JSON of province-level scores. One run produces per-dimension choropleth maps (Albers projection, editable freeform polygons), a combined ranking bar slide, a dimension matrix table, and reason/shortcoming pages. Triggers: 数据地图PPT, 省份评分地图, 中国地图 PPT, score map, choropleth, 省级政策图谱, 15省图谱."
license: MIT
metadata:
  version: "1.0"
  category: productivity
---

# 数据地图 PPT 生成器（data-map-pptx）

## Overview

把「省份/地区级评分数据」一键变成**可编辑**的中国地图 PPT：地图是 python-pptx 自由多边形（每个省都能单独改色改字），表格是原生表格，文字是文本框。全程不截图、不嵌位图，导出后可在 PowerPoint 里随意改。

一套输入同时出 5 类页：

| 页类型 | 内容 | 来源 |
|--------|------|------|
| 地图页 ×N | 每个评分维度一张分档着色中国地图（深=高分）+ 前三/末三 + 图例 + 南海小图 | `groups` 每个维度 |
| 综合地图页 | 按权重加权后的综合分地图 | `_config.综合.weights` |
| 综合排序条形页 | 各省原始总分降序横条（每维度一段颜色） | 自动 |
| 维度矩阵表页 | 省份 × 各评级档位（彩色格）+ 各维度总分 | 自动 |
| 依据与短板页 | 每个维度的评分依据 + 关键短板 | `依据_<维度>`、`短板` 字段 |
| 评级规则页 | 评分规则说明（可省略） | `_config.rule` |

## 依赖

- `pip install python-pptx`（唯一硬依赖）
- 验证可选：本机装有 PowerPoint 时可导出 PNG 目检

## 快速上手

```bash
# 1. 按 data-schema.md 准备数据（见 examples/example_data.json）
# 2. 运行（脚本在 scripts/ 下）
cd scripts
python gen_pptx.py ../examples/example_data.json ../examples/output/example.pptx
```

产出 `example.pptx`，10 页全原生可编辑对象。

## 工作流

### Step 1 准备数据

一个 JSON，结构见 [references/data-schema.md](references/data-schema.md)。核心两点：

- 省份节：`省名 → {score_<维度>: 分数, 评级_<维度>: "第一档"..., 依据_<维度>: "...", 短板: "..."}`
- 配置节 `_config`：`title` / `subtitle` / `groups`（维度聚合+满分 cap）/ `综合`（权重）/ `rule`

不会写就从 `examples/example_data.json` 复制改。**评分、评级、依据、短板全部要自己调研填真实值**，脚本只负责排版，不编数据。

### Step 2 运行

```bash
python gen_pptx.py data.json out.pptx
```

### Step 3 验证（交付前必做）

1. **结构读回**：`python-pptx` 打开，确认页数、每页自由多边形数（地图页应 ~55）、表格行列。
2. **视觉导出**（有 PowerPoint 时）：
   ```python
   import win32com.client, os
   ppt = win32com.client.Dispatch('PowerPoint.Application')
   pres = ppt.Presentations.Open(os.path.abspath('out.pptx'), WithWindow=True)
   pres.Slides(1).Export(os.path.abspath('p1.png'), 'PNG', 1200, 675)
   pres.Close(); ppt.Quit()
   ```
   用 PIL 采样地图区颜色：色阶各档应都出现、表头应为深蓝 `1F4E79`、评级格应为 `C6EFCE`→`FFC7CE` 档位色。

## 自定义

| 想改什么 | 怎么改 |
|----------|--------|
| 地图色阶 / 分档名次区间 | `geo_map.py` 的 `DEFAULT_RAMP` / `DEFAULT_BINS`（或调 `build_map(..., ramp=, bins=)`） |
| 评级档位填充色 | 数据 `_config.等级_填充`：`{"第一档": "C6EFCE", ...}` |
| 综合权重 | 数据 `_config.综合.weights`：`{"友好度": 0.4, "经济回报": 0.4, "落地": 0.2}` |
| 维度满分（cap） | `groups` 里该维度的 `cap`（默认 10；如友好度=两分项各10，cap=20） |
| 输出路径 | 第二个命令行参数 |

## 原理与限制

- 地图投影：Albers 双标准纬线 27°/45°、中央经线 105°（标准中国地图画法），代码在 `scripts/geo_map.py`，省界 GeoJSON 来自阿里 DataV（`data/china_bound.json`）。
- 只支持中国省级地图；`geo_map.py` 的 `build_map` 返回纯数据 dict（含 SVG path + 投影后环坐标），也喂得动 HTML/SVG 管线。
- 依据页按 `groups` 的 keys 映射字段：`score_用户侧` → `依据_用户侧`，自动拼接。
- 条形页刻度 = 各省原始分总和，分段时间 = 各维度原始分，序号按综合分排——**原始分排序与综合分排序可能不同**，标题会注明口径。
- 已知限制：页数随维度+省份数增长（每维度 1 地图页；依据页每 5 省 1 页），数据量大时 PPT 变长。

## 参考文件

| 文件 | 内容 |
|------|------|
| [references/data-schema.md](references/data-schema.md) | 输入 JSON 完整 schema 与字段说明 |
| [references/map-rendering.md](references/map-rendering.md) | 投影/色阶/标签/图例/南海小图规则 |
| [references/design-system.md](references/design-system.md) | PPT 版式规范（尺寸/字体/配色/页型） |
| [examples/example_data.json](examples/example_data.json) | 真实可跑的示例数据（15省，分数真实） |
