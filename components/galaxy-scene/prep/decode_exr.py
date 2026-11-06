"""Decode BlueYard ani-tiles.exr (PXR24 compression) ported from the site's own EXRLoader bundle."""
import struct, sys, zlib
import numpy as np

def read_attrs(f):
    f.seek(8)
    attrs = {}
    while True:
        b = f.read(1)
        if b == b'\x00' or b == b'':
            break
        n = b
        while (c := f.read(1)) != b'\x00':
            n += c
        t = b''
        while (c := f.read(1)) != b'\x00':
            t += c
        sz = struct.unpack('<I', f.read(4))[0]
        attrs[n.decode()] = (t.decode(), f.read(sz))
    return attrs

def parse_chlist(buf):
    chs = []
    i = 0
    names = {0: 'uint', 1: 'half', 2: 'float'}
    while i < len(buf) and buf[i] != 0:
        j = buf.index(b'\x00', i)
        name = buf[i:j].decode()
        ptype = struct.unpack('<i', buf[j+1:j+5])[0]
        chs.append({'name': name, 'type': names.get(ptype, ptype), 'ptype': ptype})
        i = j + 5 + 12
    return chs

def main(path):
    f = open(path, 'rb')
    attrs = read_attrs(f)
    x0, y0, x1, y1 = struct.unpack('<4i', attrs['dataWindow'][1])
    W, H = x1 - x0 + 1, y1 - y0 + 1
    assert attrs['compression'][1][0] == 5, 'not PXR24'
    chs = parse_chlist(attrs['channels'][1])
    print(f'{W}x{H} channels:', [(c['name'], c['type']) for c in chs])
    assert len({c['type'] for c in chs}) == 1
    is_half = chs[0]['type'] == 'half'
    print('is_half:', is_half)
    nch = len(chs)
    LINES = 16
    nchunks = (H + LINES - 1) // LINES
    offsets = struct.unpack(f'<{nchunks}Q', f.read(8 * nchunks))

    out = np.zeros((H, W, nch), dtype=np.float32)
    for ci, off in enumerate(offsets):
        f.seek(off)
        y = struct.unpack('<i', f.read(4))[0]
        dsz = struct.unpack('<i', f.read(4))[0]
        H_ = np.frombuffer(zlib.decompress(f.read(dsz)), dtype=np.uint8)
        lines = min(LINES, H - y)
        for li in range(lines):
            for chi in range(nch):
                base = (li * nch + chi) * W * 2
                if is_half:
                    p0, p1 = base, base + W
                    v = (H_[p0:p0+W].astype(np.uint32) << 8) | H_[p1:p1+W].astype(np.uint32)
                    bits = (np.cumsum(v) & 0xFFFF).astype('<u2')
                    out[y + li, :, chi] = bits.view('<f2').astype(np.float32)
                else:
                    p0, p1, p2 = base, base + W, base + 2 * W
                    v = (np.frombuffer(H_[p0:p0+W], dtype=np.uint8).astype(np.uint32) << 24) | \
                        (np.frombuffer(H_[p1:p1+W], dtype=np.uint8).astype(np.uint32) << 16) | \
                        (np.frombuffer(H_[p2:p2+W], dtype=np.uint8).astype(np.uint32) << 8)
                    bits = np.cumsum(v.astype(np.uint64)) & 0xFFFFFFFF
                    out[y + li, :, chi] = bits.astype(np.uint32).view('<f4') if False else (
                        bits.astype('<u4').view('<f4').astype(np.float32))
    np.save('pos_atlas.npy', out)
    print('min', float(out.min()), 'max', float(out.max()), 'finite', bool(np.isfinite(out).all()))
    t0 = out[0:128, 0:256]
    print('tile0 range', float(t0.min()), float(t0.max()))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'assets_2024/ani-tiles.exr')
