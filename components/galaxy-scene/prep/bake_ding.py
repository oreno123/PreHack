"""Bake galaxy->shang-ding morph atlas as pos_ding.f32 (RGBA float32, 2048x1024)."""
import numpy as np
import trimesh

TILE_W, TILE_H, TILES = 256, 128, 64
N = TILE_W * TILE_H

atlas = np.load('pos_atlas.npy')          # (1024, 2048, 3) BGR [0,1]
atlas = atlas[:, :, [2, 1, 0]]            # -> RGB
rgba = np.dstack([atlas, np.ones(atlas.shape[:2], dtype=np.float32)]).astype(np.float32)

def tile_pixels(t):
    ty, tx = t // 8, t % 8
    return rgba[ty * TILE_H:(ty + 1) * TILE_H, tx * TILE_W:(tx + 1) * TILE_W]

def smoother(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0)

mesh = trimesh.load(r'D:\desktop\纹脉\设计素材\3D打印\shang_ding_print.stl', force='mesh')
pts, _ = trimesh.sample.sample_surface(mesh, N, seed=42)
ctr = (mesh.bounds[0] + mesh.bounds[1]) / 2
pts = (pts - ctr) * (1.2 / (mesh.bounds[1][2] - mesh.bounds[0][2]))   # height -> 1.2
# stl z-up -> scene y-up: (x, y, z) -> (x, z, y)
ding = pts[:, [0, 2, 1]]
ding = (ding * 0.5 + 0.5).astype(np.float32)                          # [0,1] atlas encoding
print('ding encoded range', float(ding.min()), float(ding.max()))

gal = tile_pixels(TILES - 1)[:, :, :3].reshape(-1, 3)                 # galaxy end state

rng = np.random.default_rng(7)
delay = rng.uniform(0.0, 0.35, N)
MORPH0, HOLD = 44, 62
for k in range(MORPH0, HOLD):
    u = (k - MORPH0) / (HOLD - 1 - MORPH0)
    w = smoother((u - delay) / (1.0 - delay))[:, None]
    frame = (gal * (1 - w) + ding * w).astype(np.float32)
    tp = tile_pixels(k)
    tp[:, :, :3] = frame.reshape(TILE_H, TILE_W, 3)
for k in range(HOLD, TILES):
    tile_pixels(k)[:, :, :3] = ding.reshape(TILE_H, TILE_W, 3)

rgba.tofile('repro/data/pos_ding.f32')
print('pos_ding.f32 written', rgba.shape, rgba.nbytes // 1024 // 1024, 'MB')
