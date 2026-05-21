# 🔬 OmniAnalyser

**Universal AI Analysis Platform** — Upload any file, get intelligent analysis powered by Xiaomi MiMo V2.5

![AI](https://img.shields.io/badge/AI-MiMo%20v2.5-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tokens](https://img.shields.io/badge/daily%20tokens-8M%2B-orange)
![Python](https://img.shields.io/badge/python-3.11+-yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-brightgreen)

## Overview

OmniAnalyser is a universal file analysis platform that uses **multiple specialized AI agents** to analyze any type of file — code, documents, images, CSV data, and more. Built on Xiaomi MiMo's V2.5 series models, it provides deep insights through a 4-stage analysis pipeline.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      OmniAnalyser                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Code     │  │ Document │  │ Data     │  │ Image      │  │
│  │ Analyzer │  │ Analyzer │  │ Analyzer │  │ Analyzer   │  │
│  │(Agent 1) │  │(Agent 2) │  │(Agent 3) │  │(Agent 4)   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │
│       │              │              │              │          │
│       └──────────────┼──────────────┼──────────────┘          │
│                      ▼              ▼                         │
│              ┌─────────────────────────────┐                  │
│              │     Synthesis Engine        │                  │
│              │  Merge + Score + Recommend  │                  │
│              └─────────────┬───────────────┘                  │
│                            ▼                                  │
│              ┌─────────────────────────────┐                  │
│              │     Token Tracker           │                  │
│              │  Real-time usage dashboard  │                  │
│              └─────────────────────────────┘                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              MiMo API (OpenAI-compatible)                │ │
│  │         V2.5-Pro • V2.5-VL • V2.5-ASR • V2.5-TTS        │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Features

- **Multi-format support**: .py .js .ts .go .rs .java .pdf .csv .json .txt .png .jpg
- **4 specialized agents**: Code, Document, Data, Image — each with domain expertise
- **Real-time token dashboard**: Track consumption per-agent, per-analysis, per-day
- **Batch analysis**: Upload multiple files, analyze in parallel
- **Export results**: JSON, PDF, Markdown
- **Dark theme UI**: Professional, responsive, drag-and-drop upload

## Analysis Agents

| Agent | Input | What It Does | Model |
|---|---|---|---|
| **Code Analyzer** | .py .js .ts .go .rs .java | Security, style, logic, complexity scoring | MiMo V2.5-Pro |
| **Document Analyzer** | .pdf .txt .docx | Summarize, extract key points, Q&A | MiMo V2.5-Pro |
| **Data Analyzer** | .csv .json .xlsx | Statistics, anomalies, visualization suggestions | MiMo V2.5-Pro |
| **Image Analyzer** | .png .jpg .webp | Describe, OCR, detect objects, extract text | MiMo V2.5-VL |

## Token Consumption

| Scenario | Files/Day | Analysis Depth | Tokens/Day |
|---|---|---|---|
| Personal use | 5-10 | Standard | ~200K |
| Team (10 devs) | 50-100 | Deep | ~2M |
| Company (100 users) | 500+ | Deep + batch | ~8M |
| Platform (1000+ users) | 5000+ | All features | ~80M |

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your MiMo API key
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
python -m http.server 3000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze` | Analyze single file |
| POST | `/api/batch` | Batch analyze multiple files |
| POST | `/api/chat` | Ask questions about analyzed file |
| GET | `/api/stats` | Token usage statistics |
| GET | `/api/stats/history` | Usage history (7 days) |
| GET | `/api/stats/agents` | Per-agent breakdown |
| GET | `/api/health` | Health check |

## Tech Stack

- **AI**: Xiaomi MiMo V2.5-Pro, V2.5-VL
- **Backend**: Python 3.11, FastAPI, httpx
- **Frontend**: Vanilla JS, CSS3, Dark Theme
- **Deploy**: Docker-ready, any cloud

## License

MIT
