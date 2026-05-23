# YouTube Channel Plan — ListingsAI

## Channel
- Name: ListingsAI
- Email: magnustheassistant@gmail.com
- Niche: AI tools for real estate agents
- Goal: Drive traffic to listingsai.directory/tools/ → affiliate commissions

## Affiliate Partners
- ClickFunnels: 40% commission
- Jasper: 30% commission
- ManyChat: 30% commission

## Uploaded Videos

| # | Tool Name | Title | Status | Upload Date |
|---|-----------|-------|--------|-------------|
| 1 | real-estate-flyer-maker | real-estate-flyer-maker — Free Real Estate Tool Review | pending | 2026-05-21 |
| 2 | real-estate-brochure-templates | Real Estate Brochure Templates — Free AI Generator Review | uploaded | 2026-05-23 |
| 3 | real-estate-email-sequence-builder | Real Estate Email Sequence Builder — Free AI Generator Review | render_blocked | 2026-05-23 |

## Video Priority Queue

| # | Tool | Affiliate | Composition File | Status | Notes |
|---|------|-----------|-----------------|--------|-------|
| 1 | real-estate-email-sequence-builder | ManyChat (30%) | compositions/email-sequence-builder.html | RENDER_BLOCKED — SIGTRAP/cpufreq on this kernel. Published at https://hyperframes.dev/p/a4760604-57e1-4818-b506-df7319dc3891 | Needs machine with working Chrome to render |
| 2 | real-estate-business-plan-generator | ClickFunnels (40%) | compositions/business-plan-generator.html | composition_done | Script: video-04-real-estate-business-plan-generator.md |
| 3 | real-estate-contract-template | Real Estate Contract Template — Free AI Generator Review | compositions/contract-template.html | composition_done | Script: video-05-real-estate-contract-template.md |
| 4 | real-estate-fsbo-email-templates | ManyChat (30%) | pending | pending | |
| 5 | real-estate-commission-split-calculator | ClickFunnels (40%) | compositions/commission-split-calculator.html | composition_done | Script: video-06-real-estate-commission-split-calculator.md |

## Video Format
- Hook (15 sec): Problem statement + "There's a free tool for that"
- Demo (60 sec): Screen recording of tool working
- CTA (10 sec): "Try it free — link in description"

## Rendering Instructions
HyperFrames composition at: `~/hermes_modules/hyperframes-test/test-video/`
Run on a machine with working Chrome:
```bash
cd ~/hermes_modules/hyperframes-test/test-video
npm run render -- -o renders/contract-template.mp4
npm run render -- -o renders/business-plan-generator.mp4
```
Published compositions:
- email-sequence-builder: https://hyperframes.dev/p/a4760604-57e1-4818-b506-df7319dc3891

## Render Blockers
- This kernel has no working Chrome/Playwright (SIGTRAP on cpufreq sysfs)
- Both local Playwright and `--docker` flag fail with same root cause
- Obscura (headless Chrome) is running on port 9222 but HyperFrames doesn't support --cdp-url flag
- Workaround: Render on a machine with working Chrome, copy the .mp4, then upload to YouTube

## Completed This Run (2026-05-23 13:39 UTC)
- Script written: video-06-real-estate-commission-split-calculator.md
- Composition created: compositions/commission-split-calculator.html (0 errors, 6 warnings — track_density expected on this kernel)
- Plan updated: real-estate-commission-split-calculator added as video #5 (ClickFunnels affiliate)
- Render blocked: SIGTRAP/cpufreq on this kernel — needs machine with working Chrome to produce MP4

## Previous Runs
### 2026-05-23 12:00 UTC
- Script written: video-05-real-estate-contract-template.md
- Composition created: compositions/contract-template.html (0 errors, 5 warnings)
- Plan updated: real-estate-contract-template moved to composition_done
- real-estate-fsbo-email-templates added as pending #4