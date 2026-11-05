"""Pattern card -> band_height.png (2048x251, 6 periods of [flange | face]).

Proven pipeline (taotie/huiwen/yunlei, 2026-09): mask at source res ->
MaxFilter -> LANCZOS shrink to tile FIRST (low-pass kills pixel-frequency
aliasing that shreds 1152-seg per-vertex sampling) -> blur -> normalize ->
steepen ^1.4. Polarity auto: dark-bg card => bright lines are ridges;
light-bg card => dark ink lines are ridges.

Usage:
  python carve_band.py SRC --out band.png [--auto | --half 260 | --crop x0,y0,x1,y1]
                        [--thresh 140] [--polarity bright|dark|auto]
Prints line-frac; 0.05-0.35 reads best, retune --half/--crop if outside.
"""
import argparse
import os

import numpy as np
from PIL import Image, ImageFilter

W_STRIP, H_STRIP = 2048, 251
N_PERIOD, W_FLANGE = 6, 62
W_FACE = (W_STRIP - N_PERIOD * W_FLANGE) // N_PERIOD  # 279


def content_bbox(g, bg):
    mask = np.abs(g - bg) > 38
    ys, xs = np.where(mask)
    if len(xs) < 500:
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    half = max(x1 - x0, y1 - y0) // 2
    half = int(half * 1.06) + 4
    h, w = g.shape
    return (max(0, cx - half), max(0, cy - half),
            min(w, cx + half), min(h, cy + half))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--out", default=None)
    ap.add_argument("--auto", action="store_true", help="scan content bbox from border-bg")
    ap.add_argument("--half", type=int, default=260, help="centered square half-size")
    ap.add_argument("--crop", default=None, help="x0,y0,x1,y1 override")
    ap.add_argument("--thresh", type=int, default=140)
    ap.add_argument("--polarity", choices=["auto", "bright", "dark"], default="auto")
    a = ap.parse_args()

    im = np.asarray(Image.open(a.src).convert("RGB"), float)
    g_full = im.mean(2)
    h, w = g_full.shape
    border = np.concatenate([g_full[:8].ravel(), g_full[-8:].ravel(),
                             g_full[:, :8].ravel(), g_full[:, -8:].ravel()])
    bg = float(np.median(border))

    if a.crop:
        x0, y0, x1, y1 = [int(v) for v in a.crop.split(",")]
    elif a.auto:
        bb = content_bbox(g_full, bg)
        if bb is None:
            raise SystemExit("auto: no content found (border-bg scan empty), use --crop/--half")
        x0, y0, x1, y1 = bb
    else:
        c = h // 2
        x0, y0, x1, y1 = max(0, c - a.half), max(0, c - a.half), min(w, c + a.half), min(h, c + a.half)
    unit = im[y0:y1, x0:x1]
    g = unit.mean(2)
    print("crop", (x0, y0, x1, y1), "unit", unit.shape, "bg", round(bg, 1))

    pol = a.polarity
    if pol == "auto":
        pol = "bright" if bg < 128 else "dark"
    line = g > a.thresh if pol == "bright" else g < a.thresh
    frac = float(line.mean())
    print("polarity", pol, "line frac", round(frac, 3))
    if not 0.02 < frac < 0.6:
        print("WARN: line frac far from 0.05-0.35 sweet spot, retune --thresh/--crop")

    lm = Image.fromarray((line * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))
    lm = lm.resize((W_FACE, H_STRIP), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
    ridge = np.asarray(lm, float) / 255.0
    ridge = ridge / max(ridge.max(), 1e-6)
    ridge = ridge ** 1.4  # steepen so ridges read as cast lines, not wax

    rng = np.random.default_rng(7)
    noise = rng.normal(0, 1, (H_STRIP, W_FACE))
    noise = np.asarray(Image.fromarray(((noise - noise.min()) / np.ptp(noise) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), float) / 255
    noise = (noise - noise.mean()) * 0.02
    tile = np.clip(0.15 + noise + ridge * 0.85, 0, 1)

    xs, ys = np.arange(W_FLANGE), np.arange(H_STRIP)
    edge = np.sin(np.clip(xs / 8.0, 0, 1) * np.pi / 2) * np.sin(np.clip((W_FLANGE - 1 - xs) / 8.0, 0, 1) * np.pi / 2)
    vend = np.sin(np.clip(ys / 14.0, 0, 1) * np.pi / 2) * np.sin(np.clip((H_STRIP - 1 - ys) / 14.0, 0, 1) * np.pi / 2)
    fl = np.clip((edge[None, :] * 0.9 + 0.1) * vend[:, None], 0, 1)

    strip = np.concatenate([fl, tile] * N_PERIOD + [np.zeros((H_STRIP, W_STRIP - N_PERIOD * (W_FLANGE + W_FACE)))], axis=1)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.src)), "band_height.png")
    Image.fromarray((strip * 255).astype(np.uint8)).save(out)
    print("saved", out, "strip mean", round(float(strip.mean()), 3))


if __name__ == "__main__":
    main()
