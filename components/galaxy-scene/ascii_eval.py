"""ASCII-render sweep screenshots to find the profile-angle moment of the horse."""
from PIL import Image
import numpy as np

chars = ' .:-=+*#%@'

def show(name, rows=24, cols=78):
    a = np.asarray(Image.open(name).convert('L'), dtype=np.float32) / 255.0
    H, W = a.shape
    ys, xs = np.where(a > 0.25)
    w = (xs.max() - xs.min()) / W if len(xs) else 0
    print('--- %s  width=%.0f%%  mean=%.3f ---' % (name, 100 * w, a.mean()))
    for r in range(rows):
        line = ''
        for c in range(cols):
            v = a[int(r * H / rows):int((r + 1) * H / rows),
                  int(c * W / cols):int((c + 1) * W / cols)].mean()
            line += chars[min(max(int(v * 9.99), 0), 9)]
        print(line)

if __name__ == '__main__':
    import sys
    for n in sys.argv[1:]:
        show(n)
