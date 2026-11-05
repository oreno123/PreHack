# -*- coding: utf-8 -*-
"""中国省级评分地图·通用模块：GeoJSON 省界 → Albers 等积投影 → 抽稀 path → 标签/图例定位。

输入：省份评分字典（省短名 → 分数）+ 排序 + 名次；输出：可直接喂给 python-pptx(自由多边形)
或 HTML(SVG path) 的纯数据 dict。所有绘制逻辑与展示层解耦，HTML/PPTX 两条管线共用。

用法：
    from geo_map import build_map
    MAP = build_map(provs, scores, order, ranks,
                    bound='../data/china_bound.json',   # 省界 GeoJSON（阿里 DataV 中国地图）
                    ramp=DEFAULT_RAMP,                  # 色阶（深=高分，浅=低分），可自定
                    bins=DEFAULT_BINS)                  # 分档（名次区间 → 色阶档位），可自定

返回 dict 字段：
    W/H            画布宽高（英寸/点坐标已归一为 1000px 基准）
    main/inset     中国地图主体 + 南海小图（每条含 path 字符串 / 是否目标省 / 填充色 / 名次与分数）
    labels         省份标签（含 PIP 落点定位 + 目标省字号/分数）
    ramp/leg       色阶 + 图例条目（按名次分档，跨档省略空档）
    _rings_main    自由多边形用的原始环坐标（投影后），PPTX 版直接画
    _proj/_iproj   投影原点和缩放，供 PPTX 侧换算英寸

投影参数为"标准中国地图"写法：Albers 双标准纬线 27°/45°、中央经线 105°、中心纬线 36°。
"""

import json
import io
from math import radians, sin, cos, sqrt

# 颜色深浅 = 得分高低：深=高分（第1档），浅=低分（最末档）
DEFAULT_RAMP = ['#1F4E79', '#4A80C0', '#7FA8D8', '#AECBE8', '#D9E6F2']
# 名次分档：(起, 止) 名次区间 → RAMP 下标；BIN_RANKS 顺序即档位顺序
DEFAULT_BINS = [(1, 3), (4, 5), (6, 8), (9, 12), (13, 15)]

# Albers 等积圆锥投影
_PHI1, _PHI2, _PHI0, _LAM0 = map(radians, (27, 45, 36, 105))
_N = (sin(_PHI1) + sin(_PHI2)) / 2
_C = cos(_PHI1) ** 2 + 2 * _N * sin(_PHI1)
_RHO0 = sqrt(_C - 2 * _N * sin(_PHI0)) / _N


def albers(lon, lat):
    lam, phi = radians(lon), radians(lat)
    rho = sqrt(max(_C - 2 * _N * sin(phi), 0.0)) / _N
    th = _N * (lam - _LAM0)
    # 画布 y 轴向下，数学 y 取负——否则整图南北颠倒成"倒着的公鸡"
    return rho * sin(th), rho * cos(th) - _RHO0


def num(x):
    x = x or 0
    return int(x) if x == int(x) else x


def dp_simplify(pts, tol):
    while len(pts) > 1 and pts[0] == pts[-1]:
        pts.pop()  # 剥掉所有闭合重复点，否则 DP 基线长度为 0，整环被抽成一个点
    n = len(pts)
    keep = [False] * n
    if n:
        keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        ax, ay = pts[i]
        bx, by = pts[j]
        dx, dy = bx - ax, by - ay
        seg = (dx * dx + dy * dy) ** 0.5
        best, bi = -1.0, -1
        for k in range(i + 1, j):
            px, py = pts[k]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / seg if seg else 0.0
            if d > best:
                best, bi = d, k
        if best > tol:
            keep[bi] = True
            stack.append((i, bi))
            stack.append((bi, j))
    return [pts[k] for k in range(n) if keep[k]]


def rings_of(geom):
    if geom['type'] == 'Polygon':
        yield geom['coordinates'][0]
    else:
        for poly in geom['coordinates']:
            yield poly[0]


def short_name(full):
    for suf in ('特别行政区', '维吾尔自治区', '壮族自治区', '回族自治区', '自治区', '省', '市'):
        if full.endswith(suf):
            return full[:-len(suf)]
    return full


def pip(x, y, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def build_map(P, totals, order, ranks, bound='china_bound.json',
              ramp=DEFAULT_RAMP, bins=DEFAULT_BINS):
    """P=目标省短名集合；totals=分数；order=按分降序；ranks=名次(并列同名)。"""
    bin_of = {}
    for lo, hi in bins:
        for p in order:
            if lo <= ranks[p] <= hi:
                bin_of[p] = bins.index((lo, hi))

    bd = json.load(io.open(bound, encoding='utf-8'))
    main_rings, inset_rings = [], []  # (短名, 投影后环, 是否目标, 是否九段线)
    for f in bd['features']:
        nm = f['properties'].get('name', '')
        tgt = short_name(nm) in P if nm else False
        if not nm:  # 九段线 → 南海小图
            for r in rings_of(f['geometry']):
                if len(r) > 3:
                    inset_rings.append(('', [albers(*p) for p in dp_simplify(r, 0.008)], False, True))
            continue
        for r in rings_of(f['geometry']):
            lats = [p[1] for p in r]
            w = (max(p[0] for p in r) - min(p[0] for p in r)) * 0.82
            h = max(lats) - min(lats)
            if w * w + h * h < 0.05:  # 极小碎片（南海诸岛点缀）跳过
                continue
            simp = [albers(*p) for p in dp_simplify(r, 0.012)]
            if min(lats) >= 17:
                main_rings.append((short_name(nm), simp, tgt, False))
            else:
                inset_rings.append((short_name(nm), [albers(*p) for p in dp_simplify(r, 0.008)], tgt, False))

    def pack(rings, W, margin=8):
        xs = [x for _, r, _, _ in rings for x, _ in r] or [0]
        ys = [y for _, r, _, _ in rings for _, y in r] or [0]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        sc = (W - 2 * margin) / (x1 - x0)
        H = int((y1 - y0) * sc + 2 * margin) + 1
        return x0, y0, sc, H

    mx0, my0, msc, mH = pack(main_rings, 1000)
    ix0, iy0, isc, iH = pack(inset_rings, 300)

    def path_str(ring, x0, y0, sc):
        return 'M' + ' L'.join('%.1f,%.1f' % ((x - x0) * sc, (y - y0) * sc) for x, y in ring) + ' Z'

    main_shapes = []
    for nm, ring, tgt, _ in main_rings:
        sh = {'n': nm, 'p': path_str(ring, mx0, my0, msc), 't': tgt,
              'f': ramp[bin_of[nm]] if tgt else '#EFEFEF', 'ring': ring}
        if tgt:
            sh['s'], sh['r'] = num(totals[nm]), ranks[nm]
        main_shapes.append(sh)

    inset_shapes = [{'p': path_str(r, ix0, iy0, isc), 't': t, 'jd': jd, 'ring': r}
                    for nm, r, t, jd in inset_rings]

    # 标签：全部省级单位（港澳略）；目标省=名+分数，其余=小字灰名
    # 定位：bbox中心→顶点均值→网格扫描，PIP 确保落省内；窄省降字号
    SKIP_LABEL = ('香港', '澳门')
    best_ring = {}
    for nm, ring, tgt, _ in main_rings:
        if not nm or nm in SKIP_LABEL:
            continue
        area = (max(x for x, _ in ring) - min(x for x, _ in ring)) * (max(y for _, y in ring) - min(y for _, y in ring))
        if nm not in best_ring or area > best_ring[nm][0]:
            best_ring[nm] = (area, ring)
    labels = []
    for nm, (_, ring) in best_ring.items():
        tgt = nm in P
        xs = [x for x, _ in ring]
        ys = [y for _, y in ring]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        cand = [((x0 + x1) / 2, (y0 + y1) / 2), (sum(xs) / len(xs), sum(ys) / len(ys))]
        cx = cy = None
        for c in cand:
            if pip(*c, ring):
                cx, cy = c
                break
        if cx is None:
            for fy in (0.35, 0.5, 0.65):
                for fx in (0.35, 0.5, 0.65):
                    c = (x0 + fx * (x1 - x0), y0 + fy * (y1 - y0))
                    if pip(*c, ring):
                        cx, cy = c
                        break
                if cx:
                    break
        if cx is None:
            cx, cy = cand[0]
        vw = (x1 - x0) * msc
        if tgt:
            fs = 13 if vw >= 56 else (11 if vw >= 40 else 9.5)
        else:
            fs = 9 if vw >= 34 else 7.5
        lab = {'n': nm, 't': tgt, 'fs': fs, 'x': round((cx - mx0) * msc, 1), 'y': round((cy - my0) * msc, 1)}
        if tgt:
            lab.update({'s': num(totals[nm]), 'r': ranks[nm], 'b': bin_of[nm]})
        labels.append(lab)

    # 方向自检：北在上（黑龙江 y<广东 y）、东在右（江苏 x>新疆 x），颠倒立即报错
    _lab = {l['n']: l for l in labels}
    assert _lab['黑龙江']['y'] < _lab['广东']['y'] - 100, '地图南北颠倒！'
    assert _lab['江苏']['x'] > _lab['新疆']['x'] + 200, '地图东西颠倒！'

    leg = []
    for lo, hi in bins:
        ss = [p for p in order if lo <= ranks[p] <= hi]
        if not ss:  # 并列导致名次跳过，整段无省份 → 图例跳过该段
            continue
        vals = [totals[p] for p in ss]
        r1, r2 = ranks[ss[0]], ranks[ss[-1]]  # order 按分降序 → 段内名次递增
        seg = ('%s名' % r1) if r1 == r2 else ('第%d-%d名' % (r1, r2))
        rng = '%g' % min(vals) if min(vals) == max(vals) else '%g-%g' % (min(vals), max(vals))
        leg.append({'c': ramp[bins.index((lo, hi))], 't': '%s（%s分）' % (seg, rng)})
    return {'W': 1000, 'H': mH, 'main': [{k: v for k, v in s.items() if k != 'ring'} for s in main_shapes],
            'inset': [{k: v for k, v in s.items() if k != 'ring'} for s in inset_shapes],
            'iW': 300, 'iH': iH, 'labels': labels, 'ramp': ramp, 'leg': leg,
            '_proj': (mx0, my0, msc), '_iproj': (ix0, iy0, isc),
            '_rings_main': [(s['n'], s['ring'], s['t'], s['f']) for s in main_shapes],
            '_rings_inset': [(s['ring'], s['jd']) for s in inset_shapes]}
