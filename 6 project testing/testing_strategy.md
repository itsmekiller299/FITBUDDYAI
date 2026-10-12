# Unit Test & Integration Test Strategy

## Test Pyramid

- **70% Unit Tests** – Isolated logic for services, schemas, utilities.
- **20% Integration Tests** – End-to-end flows through API (plan generation → storage → feedback).
- **10% E2E/Playwright Tests** – UI interactions, auth flows, integrations.

## Unit Test Focus Areas

| Module | Key Functions | Test Coverage |
|--------|---------------|---------------|
| `auth` | `create_access_token`, `verify_token`, `oauth2_login` | 100% |
| `ai/client` | `generate_workout_plan`, retry logic, cost logging | 80% |
| `plans/services` | `create_plan`, `update_feedback`, `get_user_plan` | 90% |
| `exercises/models` | CRUD operations, search filters | 100% |
| `tracking/services` | `log_session`, `get_progress` | 85% |
| `config` | `Settings` validation, env loading | 100% |

## Integration Test Focus Areas

| Flow | Description | Success Criteria |
|------|-------------|------------------|
| **Plan Lifecycle** | Generate plan → log session → give feedback → plan auto-adjusts | Plan structures update correctly; RPE reflected in next session. |
| **User Onboarding** | OAuth login → profile save → first plan generation | User redirected; profile persisted; plan returns. |
| **Exercise Search** | Filter by muscle, equipment, difficulty | Correct subset returned; no irrelevant results. |
| **Integration Sync** | Apple Health callback → data import → progress update | Activities imported; progress metrics reflect. |

## Test Cases Table

| Test ID | Module | Input | Expected Output | Pass/Fail Criteria |
|---------|--------|-------|-----------------|--------------------|
| **TC-001** | Auth | Valid Google OAuth code | JWT access token + refresh token | Token contains `sub`, `exp`; valid for 15min. |
| **TC-002** | Auth | Invalid/malformed code | 401 Unauthorized | Error response with `code: INVALID_AUTH_CODE`. |
| **TC-003** | Plan Gen | Goals "build strength", no constraints | Structured JSON plan with 3-day split | Plan includes bench press, rows, squats; sets/reps sensible. |
| **TC-004** | Plan Gen | Goals "build strength", equipment "dumbbells only" | Plan uses only dumbbell exercises | Zero barbell/bar exercises in plan. |
| **TC-005** | Feedback | RPE 8, comments "too easy" | Plan adjusts next session weight +10% | Next session weight increased; RPE note logged. |
| **TC-006** | Exercise Search | `muscle=legs, equipment=bodyweight` | List of bodyweight leg exercises | All returned exercises target legs, no upper-body. |
| **TC-007** | Tracking Log | Session data with 3 exercises, sets/reps/weights | Record saved in DB; response `logged:true` | Row count in `session_logs` increases by 1. |
| **TC-008** | Tracking Progress | User with 4 logged sessions | Chart data: strength trend line + consistency % | Line shows upward trend; consistency >= 75%. |
| **TC-009** | Config | Missing `OPENAI_API_KEY` | Startup raises ValidationError | FastAPI app fails to start; clear error message. |
| **TC-010** | Integration | Full plan lifecycle (unit+integration) | All steps succeed within 5 seconds | End-to-end time < 5s; no data corruption. |

## Bug Reporting Guidelines

1. **Issue Template** (use GitHub Issues):
   - **Title**: Concise description of the bug.
   - **Environment**: OS, browser, app version, Python version.
   - **Steps to Reproduce**:
     1. ...
     2. ...
     3. ...
   - **Expected Behavior**: What should happen.
   - **Actual Behavior**: What actually happens.
   - **Screenshots/GIFs**: Optional but helpful.
   - **AI Cost Impact**: If applicable, note any extra token usage.

2. **Labeling**: Use labels `bug`, `enhancement`, `question`, `good first issue`.

3. **Priority**: `critical`, `high`, `medium`, `low` based on impact on users.

4. **Resolution Process**:
   - Triage within 24h by maintainers.
   - Assign to appropriate owner.
   - Fix targeted within 1 week for critical/high.
   - Write test case for bug fix (prevents regression).
   - Deploy to staging, then prod.

5. **Changelog**: All fixes recorded in `CHANGELOG.md` following Keep a Changelog format.