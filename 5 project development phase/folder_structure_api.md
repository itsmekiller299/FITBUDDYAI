# Folder Structure Breakdown

```
fitbuddy/
├── app.py                # Main entry point (FastAPI)
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
├── README.md             # Project overview & setup guide
├── src/
│   ├── __init__.py
│   ├── config.py         # Settings/configuration (pydantic-settings)
│   ├── auth/             # Authentication routes & logic
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── ai/               # AI service integrations
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   └── prompts.py
│   ├── plans/            # Plan generation, adaptation, storage
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── routes.py
│   ├── exercises/        # Exercise library management
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── media.py
│   ├── tracking/         # Progress logging & analytics
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── services.py
│   └── integrations/     # External service sync (Apple Health, Google Fit)
│       ├── __init__.py
│       └── routes.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_auth.py
│   │   ├── test_ai_client.py
│   │   └── test_schemas.py
│   └── integration/
│       ├── test_plan_lifecycle.py
│       └── test_integrations.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── heads/
│       └─ base
└── .gitignore
```

# Core Modules & Class Descriptions

## 1. `app.py` – Main Entry Point
- FastAPI instance creation.
- Middleware setup (CORS, request logging, exception handlers).
- Router inclusion (`auth`, `plans`, `exercises`, `tracking`, `integrations`).
- Startup event: database connection, cache warm-up.

```python
# src/app.py
from fastapi import FastAPI
from src.config import settings
from src.auth.routes import router as auth_router
from src.plans.routes import router as plans_router
from src.exercises.routes import router as exercises_router
from src.tracking.routes import router as tracking_router
from src.integrations.routes import router as integrations_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="FitBuddy AI",
        description="AI-powered personal fitness plan generator and tracker",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    # Routers
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(plans_router, prefix="/api/v1/plans", tags=["plans"])
    app.include_router(exercises_router, prefix="/api/v1/exercises", tags=["exercises"])
    app.include_router(tracking_router, prefix="/api/v1/tracking", tags=["tracking"])
    app.include_router(integrations_router, prefix="/api/v1/integrations", tags=["integrations"])

    @app.get("/", include_in_schema=False)
    async def root():
        return {"message": "FitBuddy API is running"}

    return app
```

## 2. `src/config.py` – Configuration
- Uses `pydantic-settings` to load env vars.
- Settings: API keys, CORS origins, database URLs, AI model parameters.

```python
# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    DATABASE_URL: str = "postgresql://localhost/fitbuddy"
    REDIS_URL: str = "redis://localhost:6379"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env"}

settings = Settings()
```

## 3. `src/auth/routes.py` – Authentication
- `POST /login` (Google OAuth callback).
- `POST /refresh` (JWT refresh).
- Depends on `fastapi.security.OAuth2PasswordBearer`.

## 4. `src/ai/openai_client.py` – AI Service
- Async wrapper around OpenAI ChatCompletion.
- Prompt templating for plan generation, feedback adaptation.
- Error handling, retry logic, cost logging.

```python
# src/ai/openai_client.py
import openai
from src.config import settings

async def generate_workout_plan(user_profile: dict, goals: str, constraints: str) -> dict:
    prompt = prompts.BUILD_PLAN_PROMPT.format(
        profile=user_profile, goals=goals, constraints=constraints
    )
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return {"plan": response.choices[0].message.content}
```

## 5. `src/plans/services.py` – Plan Lifecycle
- `create_plan(user_id, profile)` → generates and stores plan.
- `update_plan_feedback(plan_id, rpe, comments)` → triggers Celery task to adjust upcoming sessions.
- `get_user_plan(user_id)` → returns active plan with modifications.

## 6. `src/exercises/models.py` – Exercise Database
- SQLAlchemy model: `id`, `name`, `muscle_group`, `equipment`, `difficulty`, `demo_url`.
- CRUD routes for admin seeding and user search.

## 7. `src/tracking/services.py` – Progress Tracking
- `log_session(plan_id, session_number, completed_exercises)` → records sets/reps/weights.
- `get_progress(user_id)` → returns charts data (volume, strength gain over time).

## 8. `src/integrations/routes.py` – Service Sync
- `GET /apple-health/callback` → handle OAuth, fetch activity data.
- `POST /google-fit/sync` → import workouts/steps.

# API Specifications / Endpoint Documentation

## Base URL
`https://api.fitbuddy.ai/v1` (production) or `http://localhost:8000/v1` (dev)

## Authentication
- **OAuth2 flow** with Google.
- JWT access token (`expires` 15min) and refresh token (`expires` 30 days).
- Bearer token sent in `Authorization: Bearer <token>` header.

## Public Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/health` | Health check | None |
| `GET` | `/` | Root welcome | None |
| `POST` | `/auth/login` | Initiate Google OAuth login | None |
| `GET` | `/auth/callback` | OAuth callback handler | None |

## Protected Endpoints (Require Bearer Token)

### Plans

| Method | Endpoint | Input | Output | Description |
|--------|----------|-------|--------|-------------|
| `POST` | `/plans/generate` | `{ "goals": str, "constraints": str, "equipment": [str], "duration_min": int }` | `{ "plan_id": int, "weekly_structure": [...] }` | Generate AI-powered plan |
| `GET` | `/plans/{plan_id}` | – | `{ "days": [...], "status": str }` | Retrieve plan details |
| `POST` | `/plans/{plan_id}/feedback` | `{ "rpe": int, "comments": str }` | `{ "message": str }` | Submit session feedback; auto-adjust plan |

### Exercises

| Method | Endpoint | Input | Output | Description |
|--------|----------|-------|--------|-------------|
| `GET` | `/exercises` | `?muscle=chest&equipment=dumbbell&level=beginner` | `[{ id, name, demo_url, ... }]` | Search exercise library |
| `GET` | `/exercises/{id}` | – | `{ id, name, ... , demo_url }` | Get exercise detail |

### Tracking

| Method | Endpoint | Input | Output | Description |
|--------|----------|-------|--------|-------------|
| `POST` | `/tracking/log` | `{ "plan_id": int, "session": int, "exercises": [{ "exercise_id": int, "sets": int, "reps": int, "weight": float }] }` | `{ "logged": bool }` | Log completed session |
| `GET` | `/tracking/progress/{user_id}` | – | `{ "strength_trend": [...], "consistency": float }` | Retrieve progress analytics |

### Integrations

| Method | Endpoint | Input | Output | Description |
|--------|----------|-------|--------|-------------|
| `GET` | `/integrations/apple-health/url` | – | `{ "auth_url": str }` | Initiate Apple Health OAuth |
| `POST` | `/integrations/google-fit/sync` | `{ "access_token": str }` | `{ "imported": int }` | Sync workouts from Google Fit |

## Error Response Format
```json
{
  "detail": "Specific error message",
  "code": "ERR_001",
  "status": 400
}
```

## Rate Limiting
- **Default**: 60 requests/minute per IP.
- **Plan generation**: 10 requests/minute per user (to control AI costs).