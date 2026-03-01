# 🧭 PROJECT RULES (CORE AGENT DIRECTIVE)

> **Agent Instructions:** This is your primary source of truth. You should be good to go with just this document for general development.
> - **STANDARDS_DOC.md**: Read ONLY for deeper code examples. Use its top index (lines 1-22) to fetch ONLY the specific line ranges you need. Do NOT read the whole file.
> - **LEARNINGS.md**: Read EXCLUSIVELY when executing bug fixes or refactoring.

---

## 1. Architecture & Deployment
- **Cloud-First**: We deploy to the cloud (Railway) from the get-go.
- **Prototype == Production**: There is minimal difference between prototype and production. Build robustly from day one.
- **Monolithic-first**: Single deployable with internal modules. Extract services only when justified by massive scaling needs.
- **Database connections**: Use Direct Connection : Switch to using a Python script that connects directly to the DB. Create a db backup prior to migration. 
- **Database migrations**: Use Alembic for database migrations. Store migration files in `/migrations/`.

## 2. Configuration (The Control Center)
- **MUST** use config files (`/config/{env}.yaml` or `.env`) as the absolute control center for modifying all global variables, thresholds, toggles, and feature values.
- **NEVER** hardcode URLs, API keys, or application thresholds in the source code.

## 3. Error Handling & Logging
- **Standardized from Day 1**: Error handling must be standard and detailed from the start.
- **Format**: All errors must return `{ error: { code, message, details, trace_id, timestamp } }`.
- **Storage & Searchability**: Error logs must be stored in an easy-to-access, easily searchable file or datatable. This should be delegated (partially or fully) to an external logging/monitoring service (e.g., Sentry, Datadog) immediately.
- **NEVER** fail silently.

## 4. API Contracts & Database
- **Contracts**: Document all API contracts (OpenAPI/GraphQL/gRPC) before implementation. Store in `/contracts/`.
- **Database**: Normalize transactional data. Version all schema changes via migrations (`{timestamp}_{desc}.sql`). 

## 5. Code Conventions & UI
- **Naming**: `snake_case` (vars/funcs/files), `PascalCase` (classes/types), `UPPER_CASE` (constants). React hooks use `use*`.
- **Frontend**: Define colors/spacing in `theme.yaml`. Use relative units (rem/em).

---
**Need Examples?** → Go to `STANDARDS_DOC.md` (Read lines 1-22 to find your specific section).
**Fixing a Bug?** → Go to `LEARNINGS.md`.