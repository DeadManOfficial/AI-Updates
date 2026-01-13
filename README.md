<div align="center">

# AI Updates

### Daily Intelligence Briefs on the AI Ecosystem

[![Updates](https://img.shields.io/badge/Updates-Daily-success?style=for-the-badge)](https://github.com/DeadManOfficial/AI-Updates)
[![Coverage](https://img.shields.io/badge/Coverage-5_Companies-blue?style=for-the-badge)](https://github.com/DeadManOfficial/AI-Updates)
[![Automation](https://img.shields.io/badge/Automation-GitHub_Actions-purple?style=for-the-badge)](https://github.com/DeadManOfficial/AI-Updates)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Curated daily briefings on OpenAI, Anthropic, Google, and the wider AI landscape.**

*Wake up to summarized AI news. No noise, just signal.*

</div>

---

## Why Use This?

| Problem | Solution |
|---------|----------|
| AI news is scattered across dozens of sources | **Single daily briefing** with everything that matters |
| Hours wasted reading redundant coverage | **Summarized with impact notes** - know why it matters |
| Missing important announcements | **Automated daily updates** at 07:30 UTC |
| No context on how news affects your work | **Curated by an engineer** who uses these tools daily |

---

## Quick Start

### Read Today's Briefing

```bash
# Clone the repo
git clone https://github.com/DeadManOfficial/AI-Updates.git
cd AI-Updates

# Open today's briefing
cat updates/$(date +%Y-%m-%d).md
```

Or just browse [updates/](./updates/) on GitHub.

---

## Coverage

| Company | What's Tracked |
|---------|---------------|
| **OpenAI** | Models, API changes, GPT updates, platform news, safety announcements |
| **Anthropic** | Claude models, API updates, research papers, product launches |
| **Google** | Gemini, AI Cloud services, research, DeepMind announcements |
| **Sora 2** | Video AI developments, capabilities, access updates |
| **Broader AI** | Policy changes, funding rounds, research breakthroughs, tooling |

---

## Briefing Format

Each daily update includes:

```markdown
# AI Briefing - 2026-01-13

## OpenAI
- [Title](source-link) - Summary with impact notes

## Anthropic
- [Title](source-link) - Summary with impact notes

## Google
- [Title](source-link) - Summary with impact notes

## Broader AI
- [Title](source-link) - Summary with impact notes

---
Generated: 2026-01-13 07:30 UTC
```

---

## Repository Structure

```
AI-Updates/
├── updates/              # Daily briefings
│   ├── README.md         # Index of all updates
│   ├── 2026-01-13.md     # Today's briefing
│   ├── 2026-01-12.md     # Yesterday's briefing
│   └── ...               # Archive
├── scripts/
│   ├── update_daily.py   # Update generator
│   └── update_daily.ps1  # PowerShell variant
├── .github/workflows/
│   └── daily-update.yml  # GitHub Actions automation
└── sources.md            # Sources and methodology
```

---

## Automation

### GitHub Actions

Runs automatically at **07:30 UTC daily**:

```yaml
# .github/workflows/daily-update.yml
on:
  schedule:
    - cron: '30 7 * * *'
  workflow_dispatch:  # Manual trigger available
```

### Manual Update

```bash
# Python
python scripts/update_daily.py

# PowerShell
powershell -File scripts/update_daily.ps1
```

---

## Quick Links

| Link | Description |
|------|-------------|
| [Latest Briefing](./updates/) | Today's AI news |
| [Update Index](./updates/README.md) | Browse all briefings |
| [Sources](./sources.md) | Where we gather intel |

---

## License

Public information, curated and summarized. Use with attribution to linked sources.

---

<div align="center">

**Created by DEADMAN**

[![GitHub](https://img.shields.io/badge/DeadManOfficial-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DeadManOfficial)

*Stay ahead of AI developments. One briefing, every morning.*

</div>
