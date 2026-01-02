# AI Updates
> Daily intelligence briefs on OpenAI, Anthropic/Claude, Google/Gemini, Sora 2, and the wider AI ecosystem.

**By DeadManOfficial | Phantom Engineer**

---
## Repository Structure
```
AI-Updates/
|-- .github/
|   `-- workflows/       # Automation schedules
|-- scripts/             # Update scripts
|-- updates/             # Daily briefings + index
|   |-- README.md        # Update index
|   `-- 2025-12-20.md    # Daily briefing
`-- sources.md           # Sources + methodology
```

## Quick Links
- [Latest Briefing](./updates/2026-01-02.md)
- [Update Index](./updates/README.md)
- [Sources](./sources.md)

## Coverage
- OpenAI (models, API, platform, safety, product)
- Anthropic / Claude
- Google / Gemini (AI + Cloud)
- Sora 2 (OpenAI video)
- Broader AI news (policy, funding, research, tooling)

## Update Format
Each daily briefing includes:
- Timestamp (local + UTC if available)
- Source links
- Short summaries with impact notes

## Automation
- Local: `python scripts/update_daily.py` or `powershell -File scripts/update_daily.ps1`
- GitHub Actions: `.github/workflows/daily-update.yml` (runs daily at 07:30 UTC + manual dispatch)

## Sources and Credits
See `sources.md`.

## License
Public information, curated and summarized. Use with attribution to the linked sources.
