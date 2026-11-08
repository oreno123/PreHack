---
name: agensi-free-tools
description: Query free data tools on the Agensi marketplace (runs on Agensi official keys, no API key needed, works fine with $0 balance). Covers real-time stock quotes and company fundamentals (finnhub), academic paper search (tinyfish/treg), YouTube search, B2B company/people/email queries and counting. Use when the user asks to check a stock price/US stock ticker, search papers/literature, search YouTube, look up company profiles/contact information, or similar data retrieval needs.
---

# Agensi Free Data Tools Manual (scanned and verified 2026-11-08)

Image (9) / video (25) / voice (3) generation are all paid; free ones are all in the **data category** (~70). All called via Agensi MCP tools, official keys, zero API configuration.

## Invocation flow

```
find_tools(tool=id)   # Pull runtime parameters and example_request (mandatory for first use/uncertain parameters)
quote_tool(tool, request)  # Get quote (Free=$0; quote valid for 10 minutes)
run_tool(quote_id, confirm=true, price_usd=0)
```

- Pure Free ($0) tools: inform the user and run directly, no need to wait for consent
- Tools with a price (even "free-tier start" pricing): must wait for user's explicit consent before running
- **Freemium (free-tier start) tools require non-zero balance; blocked with $0 balance**; pure Free works fine with $0 balance

## Stock Market (finnhub, 5 tools, all free, verified usable)

| id | Purpose | Key parameters (subject to runtime find_tools) |
|---|---|---|
| `finnhub.quote` | Real-time quote (price/change) | symbol, e.g. AAPL |
| `finnhub.symbol.search` | Company name → ticker | q |
| `finnhub.company.profile` | Ticker → company profile (industry/market cap) | symbol |
| `finnhub.company.news` | Company news by date range | symbol, from, to (YYYY-MM-DD) |
| `finnhub.metrics.basic` | Fundamentals (P/E/margins/52-week range) | symbol |

## Academic Papers (2 tools)

- `tinyfish.web.search.publications` — free, verified. queryParams: `query` (required) + `domain_type=research_paper` (required) + `pub_year_min`/`pub_year_max` + `language` + `include_domains` (e.g. ["arxiv.org"]) + `after_date`/`before_date` + `page` (0-9). `fetch={}` returns the full text of each result's page along with the response. Each result includes authors/venue/citation count/pdf_url/snippet; **better coverage of latest conference papers (can find CVPR/ECCV current-year papers) than arXiv API + S2**. Actual test "SVG generation" 2024+ yielded 10 hits, all relevant.
- `treg.web.search.publications` — free-tier start $0~0.0013/call, body {q, limit}. Multi-source aggregation, falls back by cheapest. **Requires balance≠0 to use; blocked with $0 balance**.

## YouTube (4 tools, all free)

- `youtube.youtube.search.videos` — keyword video search
- `youtube.x.youtube-activities-list` — channel recent activity
- `youtube.x.youtube-members-list` — channel member list
- `youtube.x.youtube-channelsections-list` — channel page sections

## B2B (free tier, with brief descriptions)

**Search type (returns real results)**:
- `apollo.people.search` — search people by title/seniority/company/region
- `coresignal.companies.search` / `leadsforge.people.search` — return id only
- `quickenrich.people.search`, `akta.companies.search` (name/domain → id)
- `hunter.x.multi-domain-search` — search emails across companies
- `companyenrich.companies.search.preview` — first 25 results preview
- `leadsforge.companies.lookalike.preview` — lookalike company preview

**Counting/probing type (check quantity/coverage first, then decide)**:
- `companyenrich.companies.search.count`, `companyenrich.companies.similar.count`
- `icypeas.companies.search.count`, `icypeas.people.search.count`
- `getleadsio.people.search.count`, `contactout.people.count`
- `hunter.x.email-count` (emails per domain by department), `tomba.companies.emails.count`, `anymailfinder.companies.emails.count`
- `tomba.companies.emails.locations` — contact country distribution
- `contactout.people.personal_email.available` / `.work_email.available` / `.phone.available`
- `oceanio.companies.warmup` — domain coverage check

**Cached profiles** (only returns results present in cache):
- `village.companies.enrich.stored` (domain → company profile)
- `village.people.enrich.stored` (LinkedIn URL → person profile)
- `village.people.from_email.stored` (email reverse lookup)

**Autocomplete/dictionaries**:
- `companyenrich.companies.autocomplete` (company name → domain), `.positions`, `.technologies`, `.keywords.autocomplete`
- `crustdata.people.autocomplete`, `crustdata.companies.autocomplete`, `findymail.technologies.search`

**Geographic reference**: `companyenrich.geo.countries` / `.cities` / `.states.search`, `companyenrich.geo.country.get`

**Filter enumeration / task polling** (leadsforge filters ×15, companyenrich/leadsforge job status ×7, `icypeas.search.results.read`): for B2B deep usage scenarios, pull specific ids via find_tools("filters values list") etc. on demand

## Pitfalls

- find_tools multi-word query is AND semantics, may return 0 results, switch synonyms or try single words
- Exact parameters always subject to runtime `find_tools(tool=id)`; this manual only records verified or provider-declared ones
- No one has called the YouTube family yet (new tool), result format unknown, test once before bulk use
- Quotes expire in 10 minutes, re-quote after expiry (same request parameters can reuse the flow)
