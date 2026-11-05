# Scrapling 深度抓取指南

> 补充 Scout/Analyst/Financier 在 Stage 2/4/7 的深度数据采集能力。WebSearch 找源头，Scrapling 抓深度内容（PDF/表格/反爬页面/竞品官网批量）。
>
> **前置条件**：本机已装 `scrapling[all]` + 浏览器（`scrapling install` 已跑过）。所有 CLI 命令必须加 `--ai-targeted` 防 prompt injection + 自动屏蔽广告 + 抽主内容省 token。

## 何时用 WebSearch vs Scrapling

| 场景 | 用哪个 | 理由 |
|---|---|---|
| 找"有哪些行业报告" | WebSearch | 搜索引擎更全 |
| 找"美团 2024 财报 PDF 链接" | WebSearch | 知道有就行 |
| 把那份 PDF 第 47 页表格抽出来 | **Scrapling** | WebSearch 拿不到 PDF 内容 |
| 列出 5 个竞品的功能/定价/案例 | **Scrapling** | 批量抓页面 |
| 招股书里的"前五大客户收入占比" | **Scrapling** | 表格抽取 |
| 政府统计网站的具体数字 | **Scrapling** | 反爬或需要点击展开 |
| 找最新行业新闻摘要 | WebSearch | 摘要够用 |
| 某反爬行业站的会员专享内容 | **Scrapling (stealth)** | WebSearch 进不去 |

**判断口诀**：要"链接+摘要"用 WebSearch；要"具体数字+表格+全文段落"用 Scrapling。

## 反爬升级阶梯

按对抗强度逐级升级，前一级失败再升一级。速度差异小，不要为快而省：

```
scrapling extract get        # 纯 HTTP + TLS 指纹伪装，~1s
        ↓ 失败/空内容
scrapling extract fetch      # Playwright 全浏览器自动化，~3-5s
        ↓ 失败/被拦截
scrapling extract stealthy-fetch  # Stealth + Cloudflare 解决，~8-15s
```

## 模板 1：竞品官网批量抓取

**场景**：Stage 4 Competitive Landscape，要把 5 个竞品的功能/定价/案例页全部抓下来。

**CLI（推荐）**：

```bash
mkdir -p work_dir/raw_collections/competitors

# 输入 URL 列表
cat > /tmp/urls.txt <<EOF
https://competitor-a.com/pricing
https://competitor-a.com/features
https://competitor-b.com/pricing
https://competitor-c.com/case-studies
EOF

# 批量抓取（每个 URL 一个 md 文件，文件名按 URL slug）
while IFS= read -r url; do
  slug=$(echo "$url" | sed 's|https\?://||; s|/|_|g' | cut -c1-60)
  scrapling extract get "$url" "work_dir/raw_collections/competitors/${slug}.md" \
    --ai-targeted --impersonate chrome
done < /tmp/urls.txt
```

**Python（更灵活，可加 CSS 选择器）**：

```python
from scrapling.fetchers import Fetcher

urls = [
    ("competitor_a_pricing", "https://competitor-a.com/pricing", ".pricing-table"),
    ("competitor_b_features", "https://competitor-b.com/features", ".feature-grid"),
]

for slug, url, selector in urls:
    page = Fetcher.get(url, impersonate='chrome')
    if selector:
        elements = page.css(selector)
        content = "\n\n".join(e.text for e in elements)
    else:
        content = page.get_all_text()  # 全文

    out_path = f"work_dir/raw_collections/competitors/{slug}.md"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"<!-- source: {url} | fetched: 2026-MM-DD -->\n\n")
        f.write(content)
    print(f"saved {out_path} ({len(content)} chars)")
```

**输出处理**：抓完后，Analyst subagent 读所有 `competitors/*.md`，填进 `competitive_analysis.md` 的竞品矩阵表。

## 模板 2：PDF 行业报告

**场景**：Stage 2 Industry Scan，找到一份艾瑞/Frost & Sullivan/麦肯锡的 PDF 报告，要抽"市场规模""增长率""主要玩家份额"段落。

Scrapling 本身不解析 PDF。**先用 markitdown 转 md，再用 Selector 抽段落**：

```bash
# Step 1: PDF → markdown
markitdown "industry_report_2024.pdf" > work_dir/raw_collections/report_full.md

# Step 2: 抽关键段落（含"市场规模""增长率""份额"的章节）
python <<'PY'
from scrapling.parser import Selector

content = open('work_dir/raw_collections/report_full.md', encoding='utf-8').read()
page = Selector(content)

# 找所有 h1/h2 标题
for h in page.css('h1, h2, h3'):
    title = h.text.strip()
    # 关键词命中就抽取该章节
    keywords = ['市场规模', 'market size', '增长率', 'growth', '主要玩家',
                'market share', '竞争格局', 'competitive']
    if any(k in title.lower() or k in title for k in keywords):
        print(f"\n## {title}")
        # 抽下一个标题前的所有内容
        sibling = h.next_sibling
        text_parts = []
        while sibling and sibling.tag not in ('h1', 'h2', 'h3'):
            if sibling.text:
                text_parts.append(sibling.text.strip())
            sibling = sibling.next_sibling
        print("\n".join(text_parts[:10]))  # 限制 10 段
PY
```

**输出处理**：把抽出的段落整理进 `industry_scan.md`，每条数据点加 `[报告名, 年份]` 标注。

## 模板 3：反爬/Cloudflare 网站

**场景**：政府统计站、某些行业数据库、加了 Cloudflare 保护的站点。

```bash
# 单次 stealth 抓取
scrapling extract stealthy-fetch 'https://protected-site.com/data' \
  work_dir/raw_collections/protected.md \
  --ai-targeted --solve-cloudflare --css-selector '.data-table'

# 也可以 Python
python <<'PY'
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch(
    'https://protected-site.com/data',
    headless=True,
    network_idle=True,
    solve_cloudflare=True,
    google_search=False,  # 自己设 Referer
)
# 抽表格
tables = page.css('table.data-table')
for i, tbl in enumerate(tables):
    rows = tbl.css('tr')
    for row in rows:
        cells = [c.text.strip() for c in row.css('td, th')]
        print('| ' + ' | '.join(cells) + ' |')
PY
```

**StealthyFetcher 关键参数**：
- `solve_cloudflare=True` —— 解决 Cloudflare Turnstile/Interstitial
- `network_idle=True` —— 等网络空闲（JS 渲染完成）
- `headless=True` —— 无头模式
- `block_webrtc=True` —— 防 WebRTC IP 泄漏（配合代理用）
- `hide_canvas=True` —— 加 canvas 噪声防指纹

## 模板 4：财报/表格抽取

**场景**：Stage 7 Financial Model，要从年报/招股书抓具体财务表格（收入构成、成本结构、前五大客户）。

```python
"""
抓取财报表格 → 转 markdown 表格 → 喂给 Financier
"""
from scrapling.fetchers import Fetcher

# 抓年报页面（或转好 md 的招股书）
page = Fetcher.get('https://example.com/annual-report-2024', impersonate='chrome')

# 找所有表格
tables = page.css('table')
print(f"Found {len(tables)} tables")

for i, tbl in enumerate(tables):
    # 转 markdown 表格
    rows = tbl.css('tr')
    md_rows = []
    for row in rows:
        cells = []
        for c in row.css('td, th'):
            text = c.text.strip().replace('|', '\\|').replace('\n', ' ')
            cells.append(text)
        if cells:
            md_rows.append('| ' + ' | '.join(cells) + ' |')

    if len(md_rows) < 2:
        continue

    # 第一行后加分隔行
    md_rows.insert(1, '|' + '---|' * len(rows[0].css('td, th')))

    # 写文件
    with open(f'work_dir/raw_collections/table_{i}.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_rows))
    print(f"  table {i}: {len(md_rows)-1} rows × {len(rows[0].css('td, th'))} cols")
```

## 来源标注规范（满足 HARD-GATE）

Scrapling 抓到的每个数据点，进 `industry_scan.md` 时**必须**带这两项：

```markdown
## 中国光伏组件市场规模

2024 年中国光伏组件市场规模达 **¥4,200 亿**，同比增长 **23%**。

> 来源：[中国光伏行业协会 (CPIA) 2024 年度报告]
> 抓取自：https://www.cpia.org.cn/report/2024-annual.html
> 抓取时间：2026-06-16
> 原始数据：见 `work_dir/raw_collections/cpia_2024.md` 第 47 页表
```

**HARD-GATE 检查**：
- ✅ "[CPIA, 2024]" + URL + 抓取时间
- ❌ "据行业报告" （没具体出处）
- ❌ "市场规模约 X 亿"（没年份、没来源）

## 输出文件结构

```
work_dir/
├── raw_collections/              ← Scrapling 抓到的原始内容
│   ├── competitors/
│   │   ├── competitor-a_pricing.md
│   │   ├── competitor-b_features.md
│   │   └── ...
│   ├── industry_reports/
│   │   ├── cpia_2024_full.md     ← markitdown 转的全文
│   │   └── iresearch_2024.md
│   ├── tables/
│   │   ├── revenue_breakdown.md
│   │   └── top5_customers.md
│   └── collection_manifest.md    ← 所有抓取的 URL + 时间 + 状态
├── industry_scan.md              ← 整理后的引用进这里
├── market_sizing.md
└── ...
```

`collection_manifest.md` 示例：

```markdown
# 抓取清单

| URL | 模板 | 状态 | 抓取时间 | 文件 |
|---|---|---|---|---|
| https://competitor-a.com/pricing | T1 CLI | ✅ 200 | 2026-06-16 23:45 | competitors/competitor-a_pricing.md |
| https://protected-site.com/data | T3 stealth | ✅ 200 (CF solved) | 2026-06-16 23:48 | protected.md |
| industry_report.pdf | T2 PDF | ✅ 142 页 | 2026-06-16 23:50 | industry_reports/report_full.md |
```

## 常见陷阱

| 陷阱 | 症状 | 解 |
|---|---|---|
| Cloudflare 拦截 | 返回 403/503 或 challenge 页面 | 升级到 `stealthy-fetch --solve-cloudflare` |
| JS 渲染未完成 | 表格为空 / 数据缺失 | 加 `--network-idle --wait 3000` |
| PDF 表格错位 | markitdown 转出来列对不齐 | 改用 `camelot` / `tabula` 专门抽 PDF 表格 |
| Cookie 拦截 | 跳到登录页 / 404 | 加 `--cookies "k=v; k2=v2"` |
| 中文乱码 | 抓出来 ??? 或方框 | 输出文件强制 UTF-8：`encoding='utf-8'` |
| 表格合并单元格 | markdown 列数不对齐 | 接受误差，人工核对关键数字 |
| 频率太高被封 | 一段时间后 429 | 加 `--wait` 或 Python 里 `time.sleep(2)` |
| 抓到爬虫蜜罐 | 内容是假的/测试数据 | 交叉验证：同一数字至少 2 个来源 |

## 反爬合规底线

- 尊重 `robots.txt`（Scrapling 默认尊重，别手动关）
- 加 `download_delay`：批量抓 ≥ 2 秒间隔
- 不绕付费墙 / 登录墙 / 验证码（除非用户明确授权）
- 不抓个人隐私数据
- 商赛场景的"合理使用"边界：抓公开数据、引用要标注、不商业转售

## 与主流程的衔接

Scout subagent 在 Stage 2 Industry Scan 的工作流：

```
1. WebSearch 找行业报告链接、新闻、统计数据源
2. 看到需要深度内容（PDF/表格/反爬页面）→ 查本文档
3. 选对应模板（T1/T2/T3/T4）抓取
4. 抓到的原始内容存 work_dir/raw_collections/
5. 整理关键数据点进 industry_scan.md，每条加来源标注
6. Critic 审查：所有数字可追溯？来源可信？
```

不要替换 WebSearch —— 两者配合：WebSearch 找源头，Scrapling 抓深度。
