# Tools

> Companion to AGENT.md. Defines the tool surface for the agent.
> Design principle: start minimal, escalate only when needed.

## Buckets

### 1. File System
- `read_file(path)` — read text/markdown/code files
- `write_file(path, content)` — create or overwrite
- `list_dir(path)` — list files and subfolders
- `search_files(query)` — find files by name or content

### 2. Shell
- `run_command(cmd)` — execute shell commands, capture stdout/stderr
- `run_tests()` — run the project's test suite (wrapper)

### 3. Web (research)
Three jobs, three tools:
- `web_search(query)` — find what's new: product launches, exec moves, funding, filings
- `fetch_page(url)` — pull raw page content
- `extract_fields(html, schema)` — turn messy HTML into structured fields

### 4. Browser
- `browse(url)` — render JS-heavy pages, click, screenshot
- Use only when `fetch_page` returns empty or blocked content

## Tiered Research (for the 1,000-company deck)

Don't browse the open web for every company every run. Layer it:

| Tier | What | When | Cost |
|------|------|------|------|
| 1. Change detection | RSS feeds, press-release pages, SEC EDGAR, stock APIs | Every sweep | Cheap — flags only what moved |
| 2. Targeted research | `web_search` + `fetch_page` + `extract_fields` | Only on flagged deltas | Medium — deep on a few companies |
| 3. Deep dive | `browse` + multi-source cross-check | Rare, high-stakes updates | Expensive — use sparingly |

A full sweep stays cheap; a triggered update goes deep.

## Decision Table

| Scenario | Tools needed |
|----------|-------------|
| Bug fix | read, search, shell, tests |
| New feature | read, write, shell, tests |
| UI check | read, browser |
| Research task | web_search, fetch, extract |
| Company update (flagged) | web_search, fetch, extract, write |
| Company update (deep) | + browse, multi-source |

## Rules
- Read-only first. Never write before you've read.
- Never execute code you haven't inspected.
- Prefer `fetch_page` over `browse` — cheaper, faster, no JS surprises.
- Cap concurrent web calls to avoid rate limits and token blowups.
- Log every tool call: what, why, result summary.
