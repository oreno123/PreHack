# galaxy-scene · 粒子星河场景

three.js 粒子场景组件：32768 粒子的星系/器物形态，带景深、辉光、心跳节律。双击即开，VLM 评 82/100 验证过画面成立。

来自 blueyard.com 2024 粒子星河的技术考古复刻（详见 [NOTICE](NOTICE)），并在其上扩展了**任意 mesh → 粒子形态**的烘焙管线。

## 跑起来

```
双击 start.bat
→ http://localhost:8899/hybrid.html?auto=1&beat=1&shape=ding
```

URL 参数：

| 参数 | 值 | 作用 |
|---|---|---|
| `shape` | `galaxy`（默认）/ `ding` / `horse` | 粒子形态：星系 / 青铜鼎 / 翼马 |
| `beat` | `1` 心跳 / `breath` 呼吸 | 生命节律模式（不加=静态） |
| `auto` | `1` | 跳过 BEGIN 入场 |
| `clean` | `1` | 无 HUD |

实时热调按键：`[` `]` 粒子大小 · `-` `=` 曝光 · `G` 辉光 · `B` 景深 · `D` 景深 · `T` tonemap 顺序 · `H` 心跳模式 · `P` 传导波 · `E` 心电图 HUD · `S` 心音

## 三个形态怎么来的

- `galaxy`：原站动画数据解码 → 64 帧烘焙回放（大爆炸展开→成形态）
- `ding`：自有鼎 STL → trimesh 表面采样 32768 点 → 烘成帧图集 → 与星系形态 morph
- `horse`：自有翼马 GLB 同管线

**换自己的形状**：任何水密 mesh 走 `prep/bake_*.py` 管线（采样→归一化→编码→烘焙 tiles）→ `data/pos_你的形状.f32` → `?shape=你的形状`。相机 preset 按形状在 hybrid.mjs orbit 处调。

## 技术要点（复用时的关键知识）

- 粒子动画 = 烘焙纹理回放：着色器按帧取 tile，[0,1] 解码回 [-1,1]，帧间 smootherstep 插值
- **加法混合粒子的 tonemap 必须在混合之后**：每颗粒子先压再 additive 会全削顶成白；HalfFloat 累积完一次 ACES 色阶才保留
- 景深在顶点着色器做（CoC→失焦粒子放大+降透明=bokeh），不用后处理 pass
- 画面光感 = 背景星云 fbm quad + 双尺度 bloom + ACES；星点感 = 硬边缘 smoothstep + 小热核 + 暗粒子淘汰门槛
- 心跳波形用 lub-dub 双高斯，别用正弦（正弦像呼吸不像心跳）
- 截图取证：`shot_*.py`（playwright + swiftshader，无头可跑）；VLM 全挂时用 `ascii_eval.py` 自算投影看形状

## 文件

```
hybrid.html / hybrid.mjs   最终版（烘焙回放 + 光管线合体）
index.html / galaxy.mjs    纯回放版（无后处理，调试用）
three.module.js            本地 three@0.160（离线可用）
data/                      三个形状的烘焙数据 + 颜色/缩放图集
prep/                      mesh→粒子烘焙管线（bake/decode/convert）
shot_*.py ascii_eval.py    截图与评估工具
start.bat                  双击启动（http.server 8899）
NOTICE                     来源与版权说明（先读）
```
