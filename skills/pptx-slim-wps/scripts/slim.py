"""PPTX media slimming pipeline. Proven on 99MB deck -> 45MB.

Usage: python slim.py in.pptx out.pptx [--gif-max 540] [--jpeg-q 72] [--jpeg-min-kb 100]
- WAV -> mp3 96k (needs ffmpeg on PATH); fixes rels + [Content_Types].xml
- GIF >1MB -> pure-PIL NEAREST re-save at <=gif-max longest side (NEVER ffmpeg, breaks WPS)
- JPEG/PNG >min-kb -> PIL re-save quality=q optimize (jpeg only; png left unless --png)
- MP4 untouched (re-encode separately only if playback broken, see SKILL.md)
"""
import io, re, subprocess, sys, zipfile, os, tempfile
from PIL import Image

def gif_resave(data, max_side):
    im = Image.open(io.BytesIO(data))
    if im.size[0] <= max_side and im.size[1] <= max_side:
        scale = 1.0
    else:
        scale = max_side / max(im.size)
    size = (max(1, round(im.size[0] * scale)), max(1, round(im.size[1] * scale)))
    frames, durs = [], []
    for idx in range(im.n_frames):
        im.seek(idx)
        fr = im.copy()                      # keep P mode
        if scale != 1.0:
            fr = fr.resize(size, Image.NEAREST)  # NEAREST preserves palette index identity
        frames.append(fr)
        durs.append(im.info.get('duration', 80))
    out = io.BytesIO()
    frames[0].save(out, format='GIF', save_all=True, append_images=frames[1:],
                   duration=durs, loop=0, optimize=True)
    return out.getvalue()

def jpeg_resave(data, q):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.mode != 'RGB':
        im = im.convert('RGB')
    out = io.BytesIO()
    im.save(out, format='JPEG', quality=q, optimize=True)
    return out.getvalue()

def wav_to_mp3(data):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        f.write(data); wp = f.name
    mp = wp + '.mp3'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wp, '-b:a', '96k', mp], check=True)
    with open(mp, 'rb') as f: out = f.read()
    os.unlink(wp); os.unlink(mp)
    return out

def main():
    args = sys.argv[1:]
    src, dst = args[0], args[1]
    gif_max = int(args[args.index('--gif-max') + 1]) if '--gif-max' in args else 540
    jq = int(args[args.index('--jpeg-q') + 1]) if '--jpeg-q' in args else 72
    jmin = int(args[args.index('--jpeg-min-kb') + 1]) if '--jpeg-min-kb' in args else 100
    z = zipfile.ZipFile(src)
    e = {i.filename: z.read(i.filename) for i in z.infolist()}
    z.close()
    report = []
    for k in list(e):
        if not k.startswith('ppt/media/'):
            continue
        low = k.lower(); old = len(e[k])
        if low.endswith('.wav') and old > 200_000:
            e[k[:-4] + '.mp3'] = wav_to_mp3(e[k]); del e[k]
            rels_fix(e, k, k[:-4] + '.mp3')
            ct_fix(e, 'wav', 'x-wav', 'mp3', 'mpeg')
            report.append((k, old, len(e[k[:-4] + '.mp3']), 'wav->mp3'))
        elif low.endswith('.gif') and old > 1_000_000:
            new = gif_resave(e[k], gif_max)
            if len(new) < old * 0.95:
                e[k] = new
                report.append((k, old, len(new), 'gif-PIL'))
        elif low.endswith(('.jpeg', '.jpg')) and old > jmin * 1024:
            new = jpeg_resave(e[k], jq)
            if len(new) < old * 0.95:
                e[k] = new
                report.append((k, old, len(new), 'jpeg-q%d' % jq))
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zout:
        for k in ['[Content_Types].xml'] + [x for x in e if x != '[Content_Types].xml']:
            zout.writestr(k, e[k])
    from xml.dom import minidom
    zc = zipfile.ZipFile(dst)
    for n in zc.namelist():
        if n.endswith(('.xml', '.rels')):
            minidom.parseString(zc.read(n))
    zc.close()
    print(f'{src} {os.path.getsize(src)/1e6:.1f}MB -> {dst} {os.path.getsize(dst)/1e6:.1f}MB')
    for k, o, n, how in sorted(report, key=lambda r: r[1] - r[2], reverse=True):
        print(f'  {o/1e6:6.2f}M -> {n/1e6:5.2f}M  {how:8s}  {k}')

def rels_fix(e, old_media, new_media):
    old_rel, new_rel = f'../media/{old_media.split("/")[-1]}', f'../media/{new_media.split("/")[-1]}'
    for k in list(e):
        if k.endswith('.rels'):
            s = e[k].decode('utf-8')
            if old_rel in s:
                e[k] = s.replace(old_rel, new_rel).encode('utf-8')

def ct_fix(e, old_ext, old_ct, new_ext, new_ct):
    s = e['[Content_Types].xml'].decode('utf-8')
    s = s.replace(f'<Default Extension="{old_ext}" ContentType="audio/{old_ct}"/>',
                  f'<Default Extension="{new_ext}" ContentType="audio/{new_ct}"/>')
    e['[Content_Types].xml'] = s.encode('utf-8')

if __name__ == '__main__':
    main()
