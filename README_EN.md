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
2. Inspect the existing code in the real Yingdao project.
3. Copy the contents of [`project-template/`](project-template/) into the real Yingdao project root.
4. Confirm that the fixed knowledge-base path `C:\Users\Administrator\Desktop\影刀xAI开发指南` exists. Stop and ask the user for the correct path if it does not.
5. Only when adding or unable to confirm an xbot API, marketplace extension, or page behavior, use [`llms.txt`](llms.txt) to locate the relevant documentation.

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
Copy project-template files and read the project AGENTS.md
        ↓
Create TASK.md for complex work
        ↓
Use llms.txt only for new or uncertain API, extension, or page behavior
        ↓
Make the smallest required change
        ↓
Run shadowbot_sync_tool.py when adding files or when the user explicitly asks to sync Yingdao
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

The synchronization helper is stored in the real Yingdao project root. Run it after adding files. Phrases such as “sync Yingdao” or “run Yingdao sync” also mean running this command, even when only existing files changed:

```powershell
python shadowbot_sync_tool.py
```

Copy the helper from `project-template/` into the real project. The sync script scans Python files directly under the project root and does not accept a file list.

## Search keywords

Yingdao, Yingdao xbot, Yingdao RPA, Yingdao coding mode, xbot API, RPA automation, AI Agent, Agent Coding, browser automation, Excel automation, WPS automation, Windows automation, Claude Code, OpenAI Codex, Python automation.

## Contributing

Corrections, verified examples, reproducible bug reports and documentation improvements are welcome. Technical conclusions should distinguish verified behavior from unverified assumptions.

## License

MIT
