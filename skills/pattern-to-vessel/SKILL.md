---
name: pattern-to-vessel
description: "任意纹样卡 → 青铜器 3D 浮雕交互页。两步把一张纹样图片（回纹/云雷/饕餮/万字…）雕成青铜鼎腹的立体浮雕带，生成单文件 HTML（three.js，内嵌数据零依赖）：纹样浮升动画 + 纹样脱离器身径向外扩 + 剖视/七机位/绿锈棕黑双色。Triggers: 纹样上器, 雕纹样, 纹样3D, 青铜器浮雕, pattern to vessel, 纹脉器物建模."
license: MIT
metadata:
  version: "1.0"
  category: 3d
---

# 纹样上器（pattern-to-vessel）

## Overview

纹样卡图片 → 高度场 PNG → 青铜鼎浮雕带 → 单文件交互 HTML。核心是一条**已验证的低通雕刻管线**（2026-09 经 taotie/huiwen/yunlei/wanzi 四卡调通）：源分辨率建 mask → MaxFilter → **先缩到目标 tile 再模糊**（杀像素级高频，否则 1152 段逐顶点采样混叠成"碎晶噪声"）→ 归一化 → ^1.4 陡化（脊线读作铸纹而非蜡化）。

产出页面自带交互：浮雕深度滑杆、重放浮升、**纹样脱离**（纹带从器身揭下、原高度径向外扩 1.45× 成独立环+缓转）、绿锈/棕黑双色、剖视、7 机位。

## 依赖

- `pip install numpy pillow`（仅此两项；页面 three.js 走 CDN，b64 内嵌零本地文件）

## 用法（两步）

```bash
S=~/.claude/skills/pattern-to-vessel/scripts

# 1. 纹样卡 -> 高度场（自动判极性：暗底亮线=亮为脊 / 亮纸墨线=暗为脊）
python $S/carve_band.py 纹样卡.webp --auto --out band_x.png
#   看 stdout: line frac 落 0.05-0.35 最佳；超出就调 --thresh 或换 --crop x0,y0,x1,y1 / --half N

# 2. 高度场 -> 交互 HTML
python $S/make_variant.py --band band_x.png --name 回纹
#   -> ./青铜鼎-回纹版.html（--out / --desc 可覆盖）
```

手卡不对版时：VLM 报的 bbox 不可信，自己用 numpy 扫（border-bg 偏差阈值法，`--auto` 已内置）。

## 纹样选型规律（1152 段顶点位移 + 低通管线实测）

**正交几何（回纹/万字）≫ 有机曲线（云雷螺旋）＞ 复杂兽面（饕餮）**。回纹在 three.js 单边即接近 Cycles 渲染水准；饕餮五官远机位仍团块化。纹样库选型优先几何化程度高的卡。

## 模板机制

`template/ding-template.html` 由 青铜鼎-回纹版.html（2026-09-04 交互全家桶版）抽占位符而来：`__BAND_B64__`（高度场）、`__NAME__`×4（title/h1/标注/机位名）、`__DESC__`（纹样讲解词）。器型=Met 2001.210 鼎（口径17.1cm），带区 y103-125、扉棱×6、amp 5.0/4.1。改浮雕深度调模板内 `amp`；脱离外扩量调 `1 + 0.45 * d`。

## 验收

headless 截图 + VLM 双检（环绕成立/器身素面/无穿模）：

```bash
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless --disable-gpu \
  --window-size=1600,900 --screenshot="D:\abs\out.png" --virtual-time-budget=20000 \
  "file:///D:/abs/青铜鼎-X版.html?nc=1#risen&detach"
```

URL 钩子：`#risen`（跳过浮升开场）、`&detach`（脱离终态直达）、`&view=0-6`（机位）。

## 延伸

- 静帧营销图/3D 打印：同数据走 Blender Cycles 管线（约 +30% 质感），脚本在 `D:\desktop\web3d-skill-test\blender-vs-three\`（bl_build→look→env→fix→render，经 bmcp.py socket 9876），坑见 memory/reference_blender-mcp-pipeline.md。
- three.js 侧已知提效清单：envMapIntensity↑、曝光+1档、烘焙AO、高光瓣调宽柔。
