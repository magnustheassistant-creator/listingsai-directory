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
| 3 | real-estate-commission-split-calculator | Real Estate Commission Split Calculator — Free Tool Review | uploaded | 2026-05-23 |

## Video Priority Queue

| # | Tool | Affiliate | Composition File | Status | Notes |
|---|------|-----------|-----------------|--------|-------|
| 1 | real-estate-email-sequence-builder | ManyChat (30%) | compositions/email-sequence-builder.html | published | Published at https://hyperframes.dev/p/a4760604-57e1-4818-b506-df7319dc3891 |
| 2 | real-estate-business-plan-generator | ClickFunnels (40%) | compositions/business-plan-generator.html | composition_done | Script: video-04-real-estate-business-plan-generator.md |
| 3 | real-estate-contract-template | ClickFunnels (40%) | compositions/contract-template.html | composition_done | Script: video-05-real-estate-contract-template.md |
| 4 | real-estate-fsbo-email-templates | ClickFunnels (40%) | compositions/fsbo-email-templates.html | published | Script: video-09-real-estate-fsbo-email-templates.md • Published: https://hyperframes.dev/p/20ffe6a2-c9a4-47f7-aafb-15d4157bc59e |
| 5 | real-estate-flyer-maker | None (brand awareness) | compositions/flyer-maker.html | published | Script: video-07-real-estate-flyer-maker.md • Published: https://hyperframes.dev/p/3a460689-1141-4b2c-a983-a3afe5826700 |
| 6 | real-estate-buyer-lead-intake-form | ClickFunnels (40%) | compositions/buyer-lead-intake-form.html | composition_done | Script: video-08-real-estate-buyer-lead-intake-form.md • Published: https://hyperframes.dev/p/1698ba90-244d-476c-a660-67c6b5a453df |

## Video Format
- Hook (15 sec): Problem statement + "There's a free tool for that"
- Demo (60 sec): Screen recording of tool working
- CTA (10 sec): "Try it free — link in description"

## Rendering Instructions
HyperFrames composition at: `~/hermes_modules/hyperframes-test/test-video/`
Run on a machine with working Chrome:
```bash
cd ~/hermes_modules/hyperframes-test/test-video
npm run render -- -o renders/buyer-lead-intake-form.mp4
npm run render -- -o renders/business-plan-generator.mp4
npm run render -- -o renders/contract-template.mp4
```

## Published Compositions
- email-sequence-builder: https://hyperframes.dev/p/a4760604-57e1-4818-b506-df7319dc3891
- flyer-maker: https://hyperframes.dev/p/3a460689-1141-4b2c-a983-a3afe5826700
- buyer-lead-intake-form: https://hyperframes.dev/p/1698ba90-244d-476c-a660-67c6b5a453df

## Render Blockers
- This kernel has no working Chrome/Playwright (SIGTRAP on cpufreq sysfs)
- Both local Playwright and `--docker` flag fail with same root cause
- Obscura (headless Chrome) is running on port 9222 but HyperFrames doesn't support --cdp-url flag
- Workaround: Render on a machine with working Chrome, copy the .mp4, then upload to YouTube

## Completed This Run (2026-05-23 17:42 UTC)
- Script written: video-09-real-estate-fsbo-email-templates.md
- Composition created: compositions/fsbo-email-templates.html (0 errors, 1 warning — track_density)
- Published to HyperFrames: https://hyperframes.dev/p/20ffe6a2-c9a4-47f7-aafb-15d4157bc59e
- Render blocked: SIGTRAP/cpufreq on this kernel — needs machine with working Chrome to produce MP4
- FSBO Email Templates is ClickFunnels affiliate (40% recurring, 45-day cookie)
- Note: Was listed as ManyChat in queue — corrected to ClickFunnels (aligned with 50-free-tools-plan.md)

## Completed (2026-05-23 17:00 UTC)
- Script written: video-08-real-estate-buyer-lead-intake-form.md
- Composition created: buyer-lead-intake-form.html (0 errors, 1 warning — track_density)
- Published to HyperFrames: https://hyperframes.dev/p/1698ba90-244d-476c-a660-67c6b5a453df
- Render blocked: SIGTRAP/cpufreq on this kernel — needs machine with working Chrome to produce MP4
- Buyer Lead Intake Form is ClickFunnels affiliate (40% recurring, 45-day cookie)

## Completed (2026-05-23 16:41 UTC)
- Script written: video-07-real-estate-flyer-maker.md
- Composition created: compositions/flyer-maker.html (0 errors, 1 warning — track_density)
- Published to HyperFrames: https://hyperframes.dev/p/3a460689-1141-4b2c-a983-a3afe5826700
- Render blocked: SIGTRAP/cpufreq on this kernel — needs machine with working Chrome to produce MP4
- Flyer Maker has no affiliate — brand awareness play (Canva-free alternative)

## Completed (2026-05-23 13:39 UTC)
- Script written: video-06-real-estate-commission-split-calculator.md
- Composition created: compositions/commission-split-calculator.html (0 errors, 6 warnings — track_density expected on this kernel)
- Plan updated: real-estate-commission-split-calculator added as video #3 (ClickFunnels affiliate)
- Render blocked: SIGTRAP/cpufreq on this kernel — needs machine with working Chrome to produce MP4

## Previous Runs
### 2026-05-23 12:00 UTC
- Script written: video-05-real-estate-contract-template.md
- Composition created: compositions/contract-template.html (0 errors, 5 warnings)
- Plan updated: real-estate-contract-template moved to composition_done
- real-estate-fsbo-email-templates added as pending #4