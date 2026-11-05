import sys, zipfile

path = sys.argv[1] if len(sys.argv) > 1 else '.'
z = zipfile.ZipFile(path)
rows = [(i.filename, i.file_size, i.compress_size) for i in z.infolist() if i.filename.startswith('ppt/media/')]
rows.sort(key=lambda r: -r[1])
total_u = sum(r[1] for r in rows)
total_c = sum(r[2] for r in rows)
print(f'{path}: {len(rows)} media, uncompressed {total_u/1e6:.1f}MB, in-zip {total_c/1e6:.1f}MB')
print(f'{"size":>9}  {"in-zip":>9}  name')
for n, u, c in rows:
    print(f'{u/1e6:8.2f}M {c/1e6:8.2f}M  {n}')
exts = {}
for n, u, _ in rows:
    exts[n.rsplit(".", 1)[-1].lower()] = exts.get(n.rsplit(".", 1)[-1].lower(), 0) + u
print('by type:', ', '.join(f'{k} {v/1e6:.1f}M' for k, v in sorted(exts.items(), key=lambda x: -x[1])))
