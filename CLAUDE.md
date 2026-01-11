# AI Updates - Intelligence Briefs

**Identity:** Daily AI intelligence briefings repository.
**Ecosystem:** [DeadManOfficial](https://github.com/DeadManOfficial)

---

## PURPOSE

Curated daily briefings on:
- OpenAI (models, API, platform)
- Anthropic/Claude
- Google/Gemini
- Sora 2 (video AI)
- Broader AI news (policy, funding, research)

---

## STRUCTURE

```
AI-Updates/
├── updates/           # Daily briefings
│   ├── README.md      # Index
│   └── YYYY-MM-DD.md  # Daily files
├── scripts/           # Automation
└── sources.md         # Sources & methodology
```

---

## AUTOMATION

```bash
# Local update
python scripts/update_daily.py

# GitHub Actions runs daily at 07:30 UTC
```

---

## FORMAT

Each briefing includes:
- Timestamp (local + UTC)
- Source links
- Short summaries with impact notes

---

Created-By: DEADMAN
