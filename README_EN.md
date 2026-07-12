# Yingdao xbot AI Agent Development Guide

> A practical knowledge base for building and maintaining Yingdao xbot automation projects with AI coding agents.

[![AI Agent](https://img.shields.io/badge/AI-Agent-blue)]()
[![RPA](https://img.shields.io/badge/RPA-Automation-green)]()
[![xbot](https://img.shields.io/badge/xbot-Yingdao-orange)]()

[简体中文](README.md) | English

## What this repository is

This repository collects reusable documentation, rules, examples, debugging notes and workflow guidance for:

- Yingdao xbot development
- Yingdao coding-mode automation
- RPA automation engineering
- Browser automation
- Excel and WPS automation
- Windows desktop automation
- AI Agent assisted coding
- Claude Code and OpenAI Codex workflows

It is designed as a reference repository for AI coding agents and developers. It is **not** the root directory of a real Yingdao application.

## Why this project exists

Yingdao automation projects often combine visual RPA flows, Python code, browser operations, spreadsheets, Windows controls and third-party extensions. An AI coding agent needs more than a generic prompt: it needs stable rules, API references, project context and verified debugging notes.

This repository provides those materials in a structure that can be read by both humans and AI agents.

## Start here

1. Read [`AGENTS.md`](AGENTS.md) for stable repository and development rules.
2. Read [`llms.txt`](llms.txt) for the machine-readable documentation index.
3. Open [`docs/getting-started.md`](docs/getting-started.md) for the beginner workflow.
4. Use [`docs/xbot-api-guide.md`](docs/xbot-api-guide.md) to locate the correct API documentation.
5. Read the topic guides for [browser automation](docs/browser-automation.md), [Excel automation](docs/excel-automation.md) and [troubleshooting](docs/troubleshooting.md).

## Documentation

| Topic | Entry |
| --- | --- |
| Documentation index | [`docs/README.md`](docs/README.md) |
| Getting started | [`docs/getting-started.md`](docs/getting-started.md) |
| AI Agent development workflow | [`docs/ai-agent-development.md`](docs/ai-agent-development.md) |
| xbot API guide | [`docs/xbot-api-guide.md`](docs/xbot-api-guide.md) |
| Browser automation | [`docs/browser-automation.md`](docs/browser-automation.md) |
| Excel and WPS automation | [`docs/excel-automation.md`](docs/excel-automation.md) |
| Troubleshooting | [`docs/troubleshooting.md`](docs/troubleshooting.md) |
| Frequently asked questions | [`docs/faq.md`](docs/faq.md) |
| Full API reference | [`xbot-api-docs/docs/`](xbot-api-docs/docs/) |

## Recommended AI Agent workflow

```text
Describe the business goal
        ↓
Locate the real Yingdao project directory
        ↓
Read AGENTS.md and llms.txt
        ↓
Create TASK.md for complex work
        ↓
Inspect existing code and documentation
        ↓
Make the smallest required change
        ↓
Run shadowbot_sync_tool.py
        ↓
Validate inside Yingdao
```

## Main knowledge areas

### Yingdao xbot API

The repository contains organized references for browser, Excel, Windows, logging, dialogs, compression, keyboard and mouse operations, iframe extensions and selected marketplace extensions.

### Browser automation

Use the browser guide to find documentation for page objects, element lookup, clicking, input, downloads, cookies, network listening and iframe scenarios.

### Excel and WPS automation

Use the spreadsheet guide for workbook creation, reading, writing, sheet operations, range operations and formatting.

### Debugging and reverse engineering

The debugging documentation records practical ways to inspect extension source code when a marketplace command behaves differently between the visual editor and coding mode.

### AI coding agents

The repository includes conventions for Claude Code, OpenAI Codex and other agents that support `AGENTS.md` or `llms.txt`.

## Important rule

After modifying a real Yingdao project, run the synchronization helper from this knowledge-base repository:

```powershell
python "C:\path\to\yingdao-xbot-ai-agent\shadowbot_sync_tool.py" --project-dir "%LOCALAPPDATA%\ShadowBot\users\<user_id>\apps\<app_id>" prepare main.py
```

The helper belongs to this repository, not to the real Yingdao project directory.

## Search keywords

Yingdao, Yingdao xbot, Yingdao RPA, Yingdao coding mode, xbot API, RPA automation, AI Agent, Agent Coding, browser automation, Excel automation, WPS automation, Windows automation, Claude Code, OpenAI Codex, Python automation.

## Contributing

Corrections, verified examples, reproducible bug reports and documentation improvements are welcome. Technical conclusions should distinguish verified behavior from unverified assumptions.

## License

MIT
