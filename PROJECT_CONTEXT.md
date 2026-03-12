# Morning Forecast Texter — Project Context

> Last updated: 2026-03-12 by ProjDoc
> Project type: Personal Automation / SMS Notification Service

## Overview
A daily automated SMS weather forecast for McKinney, TX. Runs on GitHub Actions at 6:30 AM CST, fetches weather from Open-Meteo, optionally fetches pollen data from Ambee, and sends a formatted SMS via Twilio. Single subscriber (Chris), single Python file, zero infrastructure cost beyond Twilio SMS fees.

## Owner
- **Chris** — Creator and sole subscriber
- GitHub: `wp5frkwvhv-rgb`

## Technology / Tools
| Component | Tool | Notes |
|-----------|------|-------|
| Language | Python 3.12 | Single file, no framework |
| Weather API | Open-Meteo | Free, no key needed |
| Pollen API | Ambee | Optional, requires API key |
| SMS | Twilio | A2P 10DLC, Sole Proprietor tier |
| Scheduling | GitHub Actions | Cron: `30 12 * * *` (12:30 UTC = 6:30 AM CST) |
| Hosting | GitHub (public repo) | Required for A2P CTA URL verification |

## Twilio Configuration
All Twilio credentials and SIDs are stored in GitHub Actions Secrets and are NOT committed to this repo. See the GitHub Secrets settings for: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, MY_PHONE_NUMBER.

- **A2P Registration:** Sole Proprietor tier. Brand: APPROVED. Campaign: IN_PROGRESS (submitted 2026-03-07).
- **Phone:** 785 area code (KS)
- **Status:** Awaiting carrier campaign approval before SMS delivery can begin.

## Folder Structure
```
morning-forecast/
├── morning_forecast.py          # Main app
├── requirements.txt             # Python dependencies
├── README.md                    # [Placeholder — needs update]
├── CLAUDE.md                    # Claude working memory (this project)
├── PROJECT_CONTEXT.md           # Universal AI context (this file)
├── .github/
│   └── workflows/
│       └── daily-forecast.yml   # GitHub Actions cron job
└── docs/
    ├── privacy.md               # Privacy policy (public, A2P requirement)
    └── terms.md                 # Terms of service (public, A2P requirement)
```

## Background & Constraints
- **A2P 10DLC registration required** — US carriers mandate campaign registration for application SMS. Without approval, messages will be filtered/blocked.
- **First campaign submission failed** (late Feb 2026) due to placeholder URLs in privacy/terms fields. Campaign was deleted and resubmitted 2026-03-07 with real GitHub URLs.
- **Repo must remain public** — carrier reviewers need to access privacy policy and terms URLs at `github.com/wp5frkwvhv-rgb/morning-forecast/blob/main/docs/`.
- **No sensitive credentials in repo** — all secrets stored in GitHub Actions Secrets, injected at runtime via env vars.
- **SMS character limit** — target 280 chars. Message is truncated if it exceeds this.
- **Cost:** ~$1.50/mo for Twilio (1 SMS/day at ~$0.0079/segment + $2/mo A2P fee). GitHub Actions is free for public repos.

## Resources & Links
| Resource | URL |
|----------|-----|
| GitHub Repo | https://github.com/wp5frkwvhv-rgb/morning-forecast |
| Privacy Policy | https://github.com/wp5frkwvhv-rgb/morning-forecast/blob/main/docs/privacy.md |
| Terms of Service | https://github.com/wp5frkwvhv-rgb/morning-forecast/blob/main/docs/terms.md |
| Open-Meteo API | https://api.open-meteo.com/v1/forecast |
| Twilio Console | https://console.twilio.com |
| Ambee API (optional) | https://api.ambeedata.com |

## Changelog
| Date | Changes | Source |
|------|---------|--------|
| 2026-03-12 | Initial context created. Project scanned: 6 commits, A2P campaign in carrier review, brand approved, no errors. | ProjDoc scan + conversation history |
