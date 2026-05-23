# listingsai.directory — Pivot Plan
**Last updated:** May 20, 2026
**Status:** PHASE 1 IN PROGRESS

---

## WHY THE PIVOT

The current listingsai.directory is broken:
- Category nav buttons (Lead Generation, CRM, etc.) throw JavaScript errors on click
- 69 HTML tool files exist but none have working functionality — they're shells
- The site tries to do too much with broken JavaScript (tools loaded from tools.json, category filtering, search)
- Site has no clear value proposition — directory of broken tools = zero trust

**Revenue clarity:** Only ClickFunnels affiliate is accepted (40% recurring). Site should be built around that ONE affiliate.

---

## PHASE 1 — ClickFunnels Affiliate Hub (NOW)

### Goal
Completely rebuild listingsai.directory as a focused ClickFunnels affiliate promotion site. Clean, SEO-optimized, zero broken features.

### New Site Structure

```
listingsai.directory/
├── index.html              # Main landing page (ClickFunnels promo + content)
├── why-clickfunnels-realtors.html  # SEO article page
├── features/
│   └── (future tool pages, one at a time)
├── tools/                  # Archived 69 broken tools (hidden/disABLED)
├── styles.css
├── sitemap.xml
└── robots.txt
```

### index.html Sections
1. **Hero** — "Build Your Real Estate Empire with ClickFunnels" + CTA
2. **Problem/Aggravation** — What real estate agents struggle with (lead capture, funnels, etc.)
3. **Solution** — How ClickFunnels solves it (with specific real estate use cases)
4. **Features breakdown** — 5-6 features relevant to real estate
5. **Case study / Social proof** — Even if placeholder, makes it real
6. **ClickFunnels CTA** — Prominent affiliate link
7. **FAQ** — SEO-boosting Q&A about ClickFunnels for real estate
8. **Secondary CTA** — Bottom funnel recap

### SEO Requirements
- Full meta tags (title, description, OG, Twitter cards)
- FAQ schema markup
- Article schema on the sub-page
- Internal linking between index and article
- Fast load (no heavy JS, no external dependencies except fonts)
- Mobile responsive

### What Happens to the 69 Tools
- Move all 69 HTML files from `tools/` to `tools/archived/`
- Add a "Tools Coming Soon" notice section on the site
- These get replaced one-by-one in Phase 2

### What Happens to tools.json
- Keep for reference but don't load it dynamically on the new site
- The new Phase 2 workflow will generate working tools

### Superpowers Repo
- Cloned to `/home/hermes/superpowers/` (AI agent skill library)
- Used for Phase 2 tool development
- Not touched in Phase 1

---

## PHASE 2 — One Working Tool + One Article (Iterative)

After Phase 1 is live, repeat this cycle:

1. **Create 1 SEO article** — written content targeting a long-tail keyword
2. **Build 1 WORKING tool** — a functional HTML tool that does one thing well
3. **Test the tool** — verify it works, no errors
4. **Deploy** — push to GitHub, verify live
5. **Repeat**

### Tool Development Stack
- **Framework:** Superpowers (`/home/hermes/superpowers/`) for skill guidance
- **TDD approach:** Write the test first, then the tool
- **Single-file HTML** — keeps it simple, fast, deployable to GitHub Pages
- **One tool per article** — each tool gets a dedicated landing

### Tool Ideas (Phase 2+)
1. Real Estate ROI Calculator
2. Lead Qualification Score Calculator
3. Mortgage Payment Estimator
4. Home Staging ROI Tool
5. Listing Description Generator (the one Jasper AI tool replacement)

---

## TASKS — FULL LIST

### Phase 1 Tasks
- [ ] `design` — Design new site structure and content outline
- [ ] `build-index` — Build new index.html with all sections
- [ ] `build-article` — Create why-clickfunnels-realtors.html article page
- [ ] `archive-tools` — Move 69 broken tools to tools/archived/
- [ ] `push-phase1` — Push Phase 1 to GitHub, verify live

### Phase 2 Tasks (after Phase 1 live)
- [ ] `superpowers-setup` — Confirm Superpowers is accessible for tool dev
- [ ] `pick-keyword` — Research and pick first long-tail keyword for article
- [ ] `write-article` — Write SEO article for chosen keyword
- [ ] `build-tool-1` — Build first working tool (TDD using Superpowers)
- [ ] `test-tool` — Test tool end-to-end, fix any bugs
- [ ] `deploy-phase2` — Push tool + article, verify live
- [ ] `repeat` — Continue cycle

---

## CLICKFUNNELS AFFILIATE INFO

- **Link:** `https://www.clickfunnels.com/signup-flow?aff=108e2ab3f13e6bf0ef03c71339d2dcb330873383a8541ea451851aaf63da7380`
- **Commission:** 40% recurring for life
- **Cookie:** 45 days
- **Status:** CONFIRMED WORKING (HTTP 200)

---

## NOTES

- **Superpowers repo** (`/home/hermes/superpowers/`) is for Phase 2 tool development — do NOT open PRs against it, it's a reference library
- The 69 archived tools are NOT deleted — they exist in `tools/archived/`
- Phase 1 is about credibility and affiliate conversions, not tool quantity
- All future tools must be TESTED before deployment — no more empty shells