"""band_height PNG -> interactive bronze-ding HTML (relief rise + radial detach).

Usage:
  python make_variant.py --band band.png --name 回纹 [--out 青铜鼎-回纹版.html]
                        [--desc "annotation text"] [--template path]
"""
import argparse
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TPL = os.path.join(HERE, "..", "template", "ding-template.html")
DEFAULT_DESC = ("{n}纹带：依馆藏纹样卡测绘重绘，主纹两级浮凸。拖动「纹样浮升」，"
                "可见纹样自素地上缓缓升起——范铸纹样本是泥范刻阴、铜液填槽，脱范即成阳纹。"
                "「纹样脱离」可将纹带整体从器身揭下、沿径向外扩悬于器外。")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--band", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--desc", default=None)
    ap.add_argument("--template", default=DEFAULT_TPL)
    a = ap.parse_args()

    tpl = open(a.template, encoding="utf-8").read()
    b64 = base64.b64encode(open(a.band, "rb").read()).decode()
    html = (tpl.replace("__BAND_B64__", b64)
               .replace("__NAME__", a.name)
               .replace("__DESC__", a.desc or DEFAULT_DESC.format(n=a.name)))
    for marker in ("__BAND_B64__", "__NAME__", "__DESC__"):
        if marker in html:
            raise SystemExit("unreplaced marker: " + marker)
    out = a.out or os.path.join(os.getcwd(), "青铜鼎-%s版.html" % a.name)
    open(out, "w", encoding="utf-8").write(html)
    print("variant:", out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main()
