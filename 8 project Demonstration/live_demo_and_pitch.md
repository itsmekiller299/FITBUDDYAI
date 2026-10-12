# Comprehensive README.md Template

```markdown
# FitBuddy AI

**AI-powered personal fitness plan generator and tracker.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/itsmekiller299/FitBuddyai/blob/main/LICENSE)
[![Python 3.11](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

FitBuddy is a conversational AI fitness companion that generates personalized workout plans, adapts them based on your feedback, and tracks your progress over time. Powered by Large Language Models and integrated with popular fitness platforms, FitBuddy eliminates the need for manual program design and logging.

## Features

- **AI-Powered Plan Generation** – Describe your goals and receive a complete, periodized workout plan instantly.
- **Dynamic Adaptation** – Plans auto-adjust based on your RPE and performance feedback.
- **Exercise Library** – Searchable database with GIF/video demonstrations for proper form.
- **Progress Tracking** – Visual charts of strength gains, consistency, and volume trends.
- **Platform Integration** – Sync with Apple Health, Google Fit, and calendar apps.
- **24/7 AI Coach** – Chat-based interface to ask form questions, modify workouts, or get nutrition tips.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/itsmekiller299/FitBuddyai.git
cd FitBuddyai

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your keys (OpenAI API, Google OAuth, etc.)

# Run the development server
uvicorn app:app --reload
```

Visit `http://127.0.0.1:8000` to access the API docs (Swagger UI) and `http://127.0.0.1:3000` for the frontend (if running separately).

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis (for Celery/RQ)
- OpenAI or Anthropic API key

### Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Apply database migrations
alembic upgrade head

# Start the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (optional, if using the included React app)

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
# OpenAI / Anthropic
OPENAI_API_KEY=sk-your-openai-key-here
# ANTHROPIC_API_KEY=anthropic-key-here (optional)

# Database
DATABASE_URL=postgresql://fitbuddy:password@localhost:5432/fitbuddy

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Authentication (Google OAuth)
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# CORS (frontend origin)
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Optional: Feature flags
ENABLE_PROGRESS_TRACKING=true
ENABLE_INTEGRATIONS=true
```

## Usage

### Generating a Plan

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/plans/generate" \
  -H "Authorization: Bearer <your-jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "goals": "build overall strength",
        "constraints": "no barbell, limited time",
        "equipment": ["dumbbells", "pull-up bar"],
        "duration_min": 45
      }'
```

### Submitting Feedback

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/plans/{plan_id}/feedback" \
  -H "Authorization: Bearer <your-jwt>" \
  -H "Content-Type: application/json" \
  -d '{"rpe": 7, "comments": "feel good, could add more volume"}'
```

### Logging a Session

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/tracking/log" \
  -H "Authorization: Bearer <your-jwt>" \
  -H "Content-Type: application/json" \
  -d '{
        "plan_id": 42,
        "session": 1,
        "exercises": [
          {"exercise_id": 1, "sets": 3, "reps": 10, "weight": 135},
          {"exercise_id": 2, "sets": 3, "reps": 12, "weight": 100}
        ]
      }'
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://127.0.0.1:8000/api/docs`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc`

Generated automatically via FastAPI's `openapi` metadata.

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Write tests for new functionality.
4. Run the linter: `ruff check .` and formatter: `ruff format .`.
5. Commit your changes: `git commit -m "Add amazing feature"`.
6. Push to your fork: `git push origin feature/amazing-feature`.
7. Open a Pull Request; follow the [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

# Setup & Installation Guide

```markdown
# FitBuddy AI — Setup & Installation

## 1. Prerequisites

| Tool | Minimum Version | Notes |
|------|-----------------|-------|
| **Python** | 3.11+ | Required for FastAPI backend. |
| **PostgreSQL** | 13+ | Store user data, plans, progress. |
| **Redis** | 6+ | Required for Celery task queue & caching. |
| **Node.js** | 20+ (optional) | If running the React frontend. |
| **Git** | 2.30+ | Version control. |

## 2. Clone the Repository

```bash
git clone https://github.com/itsmekiller299/FitBuddyai.git
cd FitBuddyai
```

## 3. Create a Virtual Environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install --upgrade pip
```

## 4. Install Dependencies

```bash
cp .env.example .env   # edit .env with your keys
pip install -r requirements.txt
```

## 5. Set Up the Database

```bash
# Start PostgreSQL (Docker example)
docker run -d \
  -e POSTGRES_DB=fitbuddy \
  -e POSTGRES_USER=fitbuddy \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15

# Apply Alembic migrations
alembic upgrade head
```

## 6. Set Up Redis

```bash
# Docker
docker run -d -p 6379:6379 redis:7

# Or via Homebrew (macOS)
brew install redis
redis-server --daemonize yes
```

## 7. Run Migrations (Development Workflow)

```bash
# Create a new migration after model changes
alembic revision --autogenerate -m "describe changes"

# Apply migration
alembic upgrade head
```

## 8. Start the Application

```bash
# Development mode with auto-reload
uvicorn app:app --reload

# Or use the provided makefile (if present)
make run
```

The server will be available at `http://127.0.0.1:8000`.

## 9. Start the Frontend (Optional)

```bash
cd frontend
npm install
npm run dev   # typically runs on http://localhost:3000
```

## 10. Verify Installation

```bash
# Health check
curl http://127.0.0.1:8000/health

# Expected response: {"status": "ok"}
```
```

# Environment Variables & Configuration Guide

```markdown
# FitBuddy AI — Environment Variables & Configuration

## How to Use

1. **Copy the example file**:

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** with your values. Never commit real secrets.

## Variable Categories

### AI Provider Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Secret key for OpenAI ChatCompletion API. | `sk-proj-ABcDeFgHiJkL...` |
| `ANTHROPIC_API_KEY` (optional) | Secret key for Anthropic Claude API. | `anthropic-API-key` |
| `AI_MODEL_DEFAULT` | Default model name for plan generation. | `gpt-4o-mini` |
| `AI_TEMPERATURE` | Creativity randomness (0.0–1.0). | `0.7` |

### Database & Cache

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy-compatible PostgreSQL connection string. | `postgresql://user:pass@host:5432/dbname` |
| `REDIS_URL` | Redis connection URL for Celery/RQ. | `redis://localhost:6379/0` |

### Authentication

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_CLIENT_ID` | OAuth client ID from Google Cloud Console. | `1234567890-abcdefg.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | OAuth client secret. | `GOCSPX-...` |
| `AUTHENTICATION_BACKEND` | Fully qualified class path for custom auth backend. | `src.auth.backend:Backend` |

### CORS & Frontend

| Variable | Description | Example |
|----------|-------------|---------|
| `CORS_ORIGINS` | JSON list of allowed frontend origins (for FastAPI CORS middleware). | `["http://localhost:3000","http://localhost:8000"]` |
| `FRONTEND_URL` | Base URL of the frontend app (used in API callbacks). | `http://localhost:3000` |

### Feature Flags

| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_PROGRESS_TRACKING` | Turn progress analytics on/off. | `true` |
| `ENABLE_INTEGRATIONS` | Enable Apple Health / Google Fit sync. | `true` |
| `ENABLE_CHAT_COACH` | Activate conversational AI coach interface. | `true` |

## Loading Configuration

The backend uses **pydantic-settings** (`src/config.py`). The `Settings` class loads variables from:

1. **Environment variables** (highest priority).
2. **`.env` file** in the project root.
3. **`.env.*` files** (e.g., `.env.production`).
4. **System environment** (lowest priority).

Example:

```python
from src.config import settings

print(settings.OPENAI_API_KEY)   # reads from env/.env
print(settings.DATABASE_URL)
print(settings.CORS_ORIGINS)     # list from env string
```

## Production Checklist

- [ ] Replace placeholder values with real secrets.
- [ ] Set `DEBUG=false` (via environment or code).
- [ ] Configure a strong `SECRET_KEY` for FastAPI (handled by `python-jose` if used).
- [ ] Enable HTTPS (terminate at load balancer or via certbot).
- [ ] Set up a task scheduler (e.g., Celery Beat) for periodic jobs.
- [ ] Monitor AI token usage via provider dashboards.
- [ ] Run security scans: `bandit -r src/` and `safety check`.
```
Now phase 8: Project Demonstration.
<tool_call>
<function=write>
<parameter=content>
# Live Demo Script & Pitch Outline

## Demo Script (5‑7 minutes)

### 1. Opening (30 sec)
- **Greeting**: "Hi, I'm [Your Name] from FitBuddy AI."
- **Problem Statement**: "Most people struggle to create personalized workout plans that actually adapt as they progress."
- **Hook**: "What if your fitness plan could evolve with you, just like a personal trainer who knows your strengths and limits?"

### 2. Quick Onboarding (45 sec)
- Select goal: "Build overall strength."
- Enter constraints: "No barbell, only dumbbells and a pull‑up bar."
- Click **Generate Plan**.
- AI returns a 3‑day split with exercise names, sets/reps, and a **GIF demo** for each movement.

### 3. Plan Display & Exploration (1 min)
- Show the generated plan dashboard.
- Hover over an exercise → GIF plays inline.
- Click **Mark Complete** after a mock session.
- Submit RPE (Rate of Perceived Exertion) = 7, add comment: "Felt good, could use more volume."

### 4. Adaptation Demo (1 min)
- System auto‑adjusts the next session: weight increased by 10%, reps adjusted.
- Show the updated plan side‑by‑side with the original.
- Highlight the **feedback loop** in action.

### 5. Integration Showcase (45 sec)
- Click **Connect Apple Health** → OAuth flow → successful authorization.
- Demonstrate imported workout data appearing in the progress chart.
- Switch to **Google Fit** sync and import a sample session.

### 6. Closing & Call‑to‑Action (30 sec)
- Recap: "FitBuddy = AI generation + adaptive feedback + integrations."
- Invite questions.
- Direct to GitHub/website for early access/beta sign‑up.

## Pitch Outline (Slide‑by‑Slide)

| Slide | Title | Key Points |
|-------|-------|------------|
| 1 | **Title Slide** | FitBuddy AI – Your Adaptive Fitness Companion. |
| 2 | **The Problem** | Generic plans, no adaptation, manual logging, plateaus. |
| 3 | **Our Solution** | AI‑generated plans + real‑time adaptation + media library. |
| 4 | **How It Works** | 1️⃣ Natural‑language input → 2️⃣ LLM generation → 3️⃣ Structured storage → 4️⃣ User feedback → 5️⃣ Auto‑adjustment. |
| 5 | **Key Features** | Plan generation, dynamic adaptation, exercise GIFs, progress analytics, Apple/Google Fit sync, 24/7 chat coach. |
| 6 | **User Personas** | Beginner (guided), Trainer (fast client planning), Advanced athlete (periodization). |
| 7 | **Tech Stack** | FastAPI + React + PostgreSQL + Redis + OpenAI GPT‑4o + Docker + AWS. |
| 8 | **Market Opportunity** | $10B digital fitness market, 60% demand for personalized tech solutions. |
| 9 | **Business Model** | Freemium: free tier (3 plans/mo), Pro ($15/mo) unlimited + integrations, Trainer portal ($49/mo). |
| 10| **Roadmap** | MVP (Q2 2025) → Beta + integrations (Q3) → Public launch (Q4) → Monetization (Q1 2026). |
| 11| **Team** | Founder (AI/Full‑stack), ML Engineer, Frontend Dev, Designer. |
| 12| **Ask** | Seeking $150k seed for product development, AI cost scaling, go‑to‑market. |
| 13| **Demo** | Live (as per script above). |
| 14| **Q&A** | Open floor. |

## Key Screenshots / GIF Placeholders Breakdown

| Placeholder | Description | Usage |
|-------------|-------------|-------|
| **onboarding.png** | Wireframe-style illustration of goal/constraint selection screen. | README, pitch deck slide 2. |
| **plan_generated.png** | Screenshot of the plan grid with exercise names, GIF thumbnails, and **Mark Complete** button. | Slide 3, demo script step 3. |
| **adaptation.png** | Side‑by‑side before/after showing updated weights/reps after feedback. | Slide 4, demo step 4. |
| **integrations.png** | Mockup of connected Apple Health + Google Fit icons with data flow arrows. | Slide 5, slide 6. |
| **progress_chart.png** | Line chart visualizing strength gain over 8 weeks + consistency percentage. | Slide 5, business model slide. |
| **chat_coach.png** | Conversation bubble showing user asking "How's my form on deadlifts?" and AI response. | Slide 4, feature highlight. |
| **logo.svg** | FitBuddy word‑mark in teal/white color palette. | All slides, GitHub repo header. |

**Note**: Placeholders can be replaced with actual screenshots once the UI is built. Use `images/` folder in the repo and reference via relative paths (`./images/onboarding.png`).