"""Validate atlas visually + emit raw data for the three.js repro."""
import numpy as np
from PIL import Image

atlas = np.load('pos_atlas.npy')  # (1024, 2048, 3) BGR half→float, [0,1]
H, W, _ = atlas.shape

# --- preview: tile 0 scatter (x,y position, z as brightness) ---
tile = atlas[0:128, 0:256].reshape(-1, 3)  # BGR
rgb = tile[:, [2, 1, 0]]
pos = rgb * 2.0 - 1.0
img = np.zeros((600, 600, 3), dtype=np.uint8)
xs = ((pos[:, 0] * 0.5 + 0.5) * 599).astype(int)
ys = ((1 - (pos[:, 1] * 0.5 + 0.5)) * 599).astype(int)
ok = (xs >= 0) & (xs < 600) & (ys >= 0) & (ys < 600)
bright = np.clip((pos[:, 2] + 1) * 0.5, 0.05, 1.0)[:, None]
cols = (bright * 200).astype(np.uint8) * np.array([[0.6, 0.8, 1.3]], dtype=np.float32)
cols = np.clip(cols, 0, 255).astype(np.uint8)
np.add.at(img, (ys[ok], xs[ok]), cols[ok])
Image.fromarray(img).save('prep/preview_tile0.png')

# also tile 5 and tile 9 to see motion between frames
for t in [5, 9, 40]:
    tile = atlas[(t//8)*128:(t//8+1)*128, (t%8)*256:(t%8+1)*256].reshape(-1, 3)
    pos = tile[:, [2, 1, 0]] * 2.0 - 1.0
    img2 = np.zeros((600, 600, 3), dtype=np.uint8)
    xs = ((pos[:, 0] * 0.5 + 0.5) * 599).astype(int)
    ys = ((1 - (pos[:, 1] * 0.5 + 0.5)) * 599).astype(int)
    ok = (xs >= 0) & (xs < 600) & (ys >= 0) & (ys < 600)
    bright = np.clip((pos[:, 2] + 1) * 0.5, 0.05, 1.0)[:, None]
    cols = np.clip((bright * 200).astype(np.uint8) * np.array([[0.6, 0.8, 1.3]], dtype=np.float32), 0, 255).astype(np.uint8)
    np.add.at(img2, (ys[ok], xs[ok]), cols[ok])
    Image.fromarray(img2).save(f'prep/preview_tile{t}.png')
print('previews saved')

# --- emit raw: pos atlas as RGB float32 (R,G,B order) ---
rgbt = atlas[:, :, [2, 1, 0]].astype(np.float32)
rgbt.tofile('repro/data/pos.f32')
print('pos.f32', rgbt.shape, rgbt.nbytes // 1024 // 1024, 'MB', float(rgbt.min()), float(rgbt.max()))

# --- color-tiles.png -> raw u8 RGBA ---
c = np.array(Image.open('assets_2024/color-tiles.png').convert('RGBA'))
c.tofile('repro/data/color.rgba')
print('color', c.shape)

# --- scale-texture.png -> raw u8 RGBA ---
s = np.array(Image.open('assets_2024/scale-texture.png').convert('RGBA'))
s.tofile('repro/data/scale.rgba')
print('scale', s.shape, 'sample values', s[0, :4].tolist())
