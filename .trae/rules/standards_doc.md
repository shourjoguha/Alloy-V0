# 📚 STANDARDS & EXAMPLES (ORCHESTRATION HEADER)
> **AGENT INSTRUCTION**: DO NOT read this entire file. Read ONLY the lines corresponding to your current task.
> Rely on PROJECT_RULES.md first. Only come here for specific technical implementations.

## 📍 Orchestration Index (Lines 1-22)
| Task / Topic Category | Fetch Relevant Lines |
|-----------------------|----------------------|
| Python Backend (FastAPI, Naming, Async) | Lines 25 - 65 |
| Swift / iOS (MVVM, Architecture) | Lines 70 - 110 |
| Database Schema & Migrations | Lines 115 - 150 |
| Config Management (The Control Center) | Lines 155 - 190 |
| Error Handling & External Logging | Lines 195 - 230 |
| Cloud Deployment (Railway) & Docker | Lines 235 - 325 |
| Testing Patterns & LLM Integration | Lines 330 - 375 |

*(Agent reminder: Use tools to read ONLY the line boundaries listed above. Do not ingest the rest of the document.)*

---





# Python Backend Standards
*Lines 25-65*

## File Structure & Naming
```python
# Files/Functions: snake_case (e.g. workout_generator.py)
# Classes: PascalCase
class WorkoutPlan:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
```

## Function Documentation
```python
def calculate_volume(sets: int, reps: int, weight: float) -> float:
    """
    Calculate training volume.
    """
    return sets * reps * weight
```

## Async Pattern
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def fetch_workouts(user_id: str, db: AsyncSession) -> list[Workout]:
    async with db.begin():
        result = await db.execute(
            select(Workout).where(Workout.user_id == user_id).limit(10)
        )
        return result.scalars().all()
```


















# Swift / iOS Standards
*Lines 70-110*

## File Organization & MVVM Pattern
```swift
// Model
struct Workout: Identifiable, Codable {
    let id: UUID
    let name: String
    let duration: TimeInterval
}

// ViewModel
@MainActor
class WorkoutListViewModel: ObservableObject {
    @Published var workouts: [Workout] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    func fetchWorkouts() async {
        isLoading = true
        defer { isLoading = false }
        do {
            workouts = try await apiClient.fetchWorkouts()
        } catch {
            errorMessage = "Failed to load: \(error.localizedDescription)"
        }
    }
}
```

## Naming Conventions
```swift
// Properties: camelCase
var workoutPlan: WorkoutPlan

// Methods: camelCase with verb
func calculateOneRepMax(weight: Double, reps: Int) -> Double

// Types: PascalCase
struct WorkoutPlan {}
```













# Database Schema & Migrations
*Lines 115-150*

## Schema Standards
```sql
CREATE TABLE workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,  -- Soft delete
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    CONSTRAINT workouts_name_length CHECK (length(name) >= 3)
);

-- Always index foreign keys
CREATE INDEX idx_workouts_user_id ON workouts(user_id) WHERE deleted_at IS NULL;
```

## Migration File Template
```sql
-- Migration: 005_add_user_preferences
-- ==== UP ====
BEGIN;
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value JSONB NOT NULL
);
COMMIT;
-- ==== DOWN ====
BEGIN;
DROP TABLE IF EXISTS user_preferences CASCADE;
COMMIT;
```








# Config Management (The Control Center)
*Lines 155-190*

## Environment Files (.env)
```bash
# .env.development
DATABASE_URL=postgresql://localhost:5432/app_dev
LOG_LEVEL=DEBUG

# .env.production
DATABASE_URL=postgresql://prod-db/app_prod
LOG_LEVEL=WARNING
```

## Config Loader (Python)
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "App"
    environment: str = "development"
    database_url: str
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Centralized usage -> NEVER HARDCODE!
settings = get_settings()
print(settings.database_url)
```









# Error Handling & External Logging
*Lines 195-230*

## Standardized JSON Error Response
```python
# The absolute standard for API error responses
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Invalid input provided.",
    "trace_id": "req_abc123",
    "timestamp": "2026-02-27T12:00:00Z"
  }
}
```

## External Logging / Delegation 
```python
# Example delegating to an external service like Sentry or Datadog
def capture_exception(exception: Exception, context: dict):
    # Log to local/searchable file
    logger.error(
        f"Error: {str(exception)}", 
        extra={"context": context, "trace_id": context.get("trace_id")}
    )
    
    # Push to external service for searchability
    if settings.environment == "production":
        import sentry_sdk
        with sentry_sdk.push_scope() as scope:
            scope.set_context("app_context", context)
            sentry_sdk.capture_exception(exception)
```









# Cloud Deployment (Railway) & Docker
*Lines 235-325*

## Dockerfile for Railway Deployments
```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Railway injects $PORT automatically. Default to 8000 for local.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## railway.json (Configuration)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
```

## Docker Command Execution

```bash
# WRONG - Interactive mode causes hanging terminals
docker exec -it container_id psql -U user -d db -c "SELECT..."

# CORRECT - Non-interactive mode for automated commands
docker exec container_id psql -U user -d db -c "SELECT..."

# WRONG - Interactive mode for scripts
docker exec -it container_id psql -U user -d db -f /path/to/script.sql

# CORRECT - Non-interactive mode for scripts
docker exec container_id psql -U user -d db -f /path/to/script.sql
```

**Rule**: NEVER use `-it` flags for automated/non-interactive docker exec commands. These flags allocate a pseudo-TTY and keep STDIN open, causing terminals to hang even after command completion. Use non-interactive mode for all scripts, migrations, and automated queries. Only use `-it` for manual debugging sessions.




# Testing Patterns & LLM Integration
*Lines 330-375*

## Testing Structure (Pytest)
```python
import pytest
from services.workout import calculate_volume

def test_calculate_volume():
    result = calculate_volume(sets=5, reps=10, weight=100)
    assert result == 5000

def test_calculate_volume_zero_weight():
    result = calculate_volume(sets=5, reps=10, weight=0)
    assert result == 0
```

## LLM Call Pattern with Tenacity Retry
```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def generate_workout_llm(user_profile: dict) -> dict:
    try:
        response = await llm_client.complete(
            prompt.format(**user_profile),
            temperature=0.7
        )
        return parse_workout_json(response)
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        # Always return a fallback if all retries fail
        return get_cached_workout_template(user_profile['level'])
```
