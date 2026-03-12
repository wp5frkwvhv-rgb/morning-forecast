# Morning Forecast Texter — Claude Working Memory

> Last updated: 2026-03-12 by ProjDoc

## Current Focus
- **A2P 10DLC campaign under carrier review** — submitted 2026-03-07, status: IN_PROGRESS. No errors. Expected approval within 5-7 business days.
- SMS delivery is blocked until A2P campaign is approved by carriers.
- Once approved, the GitHub Actions cron will automatically send daily forecasts — no manual action needed.

## Key Decisions
- **Single-file architecture** — entire app is `morning_forecast.py`. Intentionally simple; no framework, no database.
- **Open-Meteo over OpenWeatherMap** — free, no API key required, reliable for daily forecasts.
- **Ambee for pollen** — optional; only activates if `AMBEE_API_KEY` is set. Currently not configured.
- **GitHub Actions for scheduling** — avoids running a server. Cron triggers at 12:30 UTC (6:30 AM CST).
- **Twilio Messaging Service** used instead of direct phone number sending — required for A2P compliance.
- **Repo made public** — required so Twilio carrier reviewers can verify privacy policy and terms URLs.

## Conventions
- All credentials via environment variables / GitHub Secrets. Never hardcoded in committed code.
- Default values in code (e.g., phone numbers) are fallbacks for local testing only.
- SMS target: 280 chars max. Truncation with "..." if exceeded.
- WMO weather codes mapped to human-readable descriptions + emoji.

## Terminology
- **A2P 10DLC** — Application-to-Person messaging over 10-digit long codes. US carrier requirement for business SMS.
- **Sole Proprietor** — Twilio low-volume A2P registration tier. $2/mo + $15 one-time campaign fee.
- **CTA** — Call to Action. Twilio/carrier term for consent verification (privacy policy + terms URLs).
- **WMO codes** — World Meteorological Organization weather condition codes returned by Open-Meteo.

## File Guide
| File | Purpose |
|------|--------|
| `morning_forecast.py` | Main app — fetches weather, builds SMS, sends via Twilio |
| `requirements.txt` | Python deps: `requests`, `twilio` |
| `.github/workflows/daily-forecast.yml` | GitHub Actions cron job (6:30 AM CST daily) |
| `docs/privacy.md` | Privacy policy (public, linked in A2P campaign) |
| `docs/terms.md` | Terms of service (public, linked in A2P campaign) |
| `README.md` | Placeholder — needs updating |

## Notes
- **Missing `.gitignore`** — should add one (Python template) to keep repo clean.
- **README.md is default placeholder** — should be updated with project description and setup instructions.
- **Fallback SMS** — if weather fetch fails, a generic "check your weather app" message is sent instead.
- **Pollen feature dormant** — Ambee API key not configured in GitHub Secrets. Can be enabled later.
- **GitHub Secrets configured:** TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, MY_PHONE_NUMBER. AMBEE_API_KEY not set.
