---
name: pptx-slim-wps
description: "Compress oversized .pptx files by slimming embedded media (WAV→mp3, GIF re-pack, JPEG re-quality, video re-encode to CFR baseline), and make media WPS-compatible (video click-play timing, GIF autoplay). Use when a .pptx is too big to send/upload, or when videos/animations don't play in WPS Office (WPS 放映). Includes a non-invasive screen-capture verification rig for WPS slideshow."
---

# PPTX 媒体瘦身 + WPS 兼容（2026-09 实测定论）

## 第一步永远是媒体清单

```bash
python scripts/inventory.py 大文件.pptx
```

经验分布（99MB 工程实例）：**WAV 背景音乐 39MB 常是最大头** > 大 GIF > 嵌入字体(.fntdata) > JPEG > mp4。先看清单再动手，别瞎压。

## 四个压缩配方（按收益排序）

1. **WAV → mp3 96k**：`ffmpeg -i audio1.wav -b:a 96k audio1.mp3`；同时改 3 处：删 `ppt/media/audio1.wav` 加 `audio1.mp3`、对应 `slideN.xml.rels` 的 Target、`[Content_Types].xml` 的 wav Default 换 mp3（`audio/mpeg`）。听感无差，39MB→0.4MB 级别。
2. **GIF 纯 PIL 重压（红线配方，见下）**：缩到显示尺寸（≤540px 边）+ NEAREST + optimize。18MB→6MB 级别。
3. **JPEG >100KB 重存**：PIL `quality=72, optimize=True`。每张省 20-40%，合计几 MB。
4. **MP4 只有在播放有问题时才重转**：`ffmpeg -i in.mp4 -vf fps=12 -fps_mode cfr -r 12 -c:v libx264 -profile:v baseline -level 3.1 -pix_fmt yuv420p -movflags faststart -an`。本来能播就别动（重转省不了多少）。

写回 zip：`[Content_Types].xml` 放第一个条目，deflate level 6，写完用 minidom 校验全部 xml/rels。

## WPS 兼容红线（全部实测）

- **WPS 无视一切 PPTX timing 树视频自动播放**。5 种 XML 变体 + WPS 自产 autoplay + COM `MediaFormat.PlayOnEntry`（属性不存在）全灭。别再试。
- **自动播放唯一通路 = GIF**（图片管线，放映和编辑视图都自动循环）。
- **视频可靠方案 = 点击播放**：timing 模板见 `scripts/video_timing.py` 的 `timing_click_only(spid)`（video_node + interactiveSeq onClick→togglePause，照 PowerPoint 模板）。
- **ffmpeg 产出的 GIF 会污染整个 deck**：一个坏 GIF → 全文件所有 GIF 冻结。GIF 重压**只能纯 PIL**：

```python
from PIL import Image
im = Image.open(src); frames, durs = [], []
idx = 0
while True:
    im.seek(idx)
    fr = im.copy()                       # 必须 copy，保 P 模式
    fr = fr.resize(size, Image.NEAREST)  # 必须 NEAREST：保调色板索引逐帧恒等，帧间 bbox-diff 才成立
    frames.append(fr); durs.append(im.info.get('duration', 80)); idx += 1
    if idx >= im.n_frames: break
frames[0].save(dst, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True)
```

- High Profile / VFR（GIF 转码常见 timebase 1/12288）mp4 在 WPS **不播**；必须 CFR + Constrained Baseline L3.1。
- `repeatCount="indefinite"` 实测不循环；视频播完 WPS 可能自动翻页；编辑视图视频永远只显示海报帧（正常）。

## 验证 rig（scripts/verify_rig.ps1）

用户在用机器时**禁止**抢前台（SetCursorPos/mouse_event）。真值通道：

1. Kwpp COM 打开 + `SlideShowSettings.Run()`
2. 放映窗 `SetWindowPos` 停靠 (vw-740, vh-520) 720×450，flags `0x0010|0x0200|0x0400`（NOACTIVATE|NOZORDER|NOSENDCHANGING）——不抢焦点不动鼠标
3. `GotoSlide(n)` 后必读 `View.Slide.SlideID` 校验落页（sldId=256+N-1，16:9 deck sldSz=8128000×4572000）
4. 同页两次间隔 1.5s `CopyFromScreen` 截图，帧差分：区域 >10% 像素变化=在动（视频 39-64%，GIF 6-34%，静图 0%）

陷阱：
- **PrintWindow 对被遮挡窗返回 DWM 冻结缓存**（md5 相同的假静止帧）——只信 CopyFromScreen 对可见窗。
- 僵尸 wpp.exe（内存 32-52K）会拒 COM（RPC_E_CALL_REJECTED）——别硬开。
- .ps1 里写中文路径会被 GBK 误读 → PowerShell 内 `Get-ChildItem` 通配符解析，或先拷 ASCII 路径。
- WPS Quit 后句柄残留 → `cp` 报 Device or resource busy，等一两分钟重试即过。
- 用户用 WPS 存过会重排 shape id / media 文件名 → 锚点用 spid 正则，别写死。
- 交付验证最强形态 = `cmp` 成品 vs 已 rig 验证的产物（字节级）。

## 完整实例

D:\tmp\pptx_fix\（rig*.ps1 + build_test*.py）：99MB 工程汇报 PPTX → 45MB 自动播放版（WAV→mp3 39MB + 3 大 GIF PIL 重压 + JPEG q72）+ 34MB 视频点击版（GIF 全转 12fps CFR mp4）。
