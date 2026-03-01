# Hyrox Staging Schema - Refined Design

## Overview
Streamlined schema with 6 tables (down from 8). Removed scraping artifacts (favorites, comments) and converted structured strings to proper types.

---

## Schema Changes

### Removed:
- `favorites_count`, `comments_count` from hyrox_workouts_staging (scraping artifacts, not core data)
- `hyrox_workout_movements_staging` table (redundant - data already in lines table)
- Bulky JSON/text columns where structured types work better

### Improved Data Types:
- `start_time`, `end_time` now use TIME type instead of VARCHAR(50)
- `time_specification` can use proper time fields
- Metric types more explicit (reps, distance, duration, calories, weight)

---

## Refined Schema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    hyrox_workouts_staging                         │
│  ──────────────────────────────────────────────────────     │
│  • id (PK)           INTEGER  AUTO_INCREMENT                   │
│  • wod_id             VARCHAR(100)   URL slug                    │
│  • name               VARCHAR(255)   Workout name                │
│  • url                TEXT    Full URL                             │
│  • badge              TEXT    Badge text                           │
│  • workout_type       ENUM           amrap/emom/for_time/...    │
│  • workout_goal       ENUM           max_rounds/finish_quickly  │
│  • time_specification  VARCHAR(100)   Text time spec                │
│  • total_time_minutes INTEGER                                          │
│  • time_cap_minutes   INTEGER                                          │
│  • has_buy_in        BOOLEAN                                          │
│  • has_cash_out      BOOLEAN                                          │
│  • is_complex        BOOLEAN    Mini circuits/ladders/time segments │
│  • full_description   TEXT    Complete workout description           │
│  • scraped_at        TIMESTAMP                                             │
│  • source_page        VARCHAR(100)                                           │
│  • status            ENUM           pending_review/reviewed/...    │
│  • notes             TEXT    Manual notes/instructions              │
└───────────────────────────┬─────────────────────────────────────────────┘
                           │ FK: workout_id
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 hyrox_workout_lines_staging                         │
│  ──────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • line_number              INTEGER  (sequence in workout)       │
│  • line_text                TEXT    (original description)       │
│  • is_rest                 BOOLEAN                                  │
│  • is_buy_in              BOOLEAN                                  │
│  • is_cash_out             BOOLEAN                                  │
│  • movement_name           VARCHAR(200)  (normalized name)    │
│  • reps                    INTEGER                                  │
│  • distance_meters         NUMERIC(10,2)                            │
│  • duration_seconds        INTEGER                                  │
│  • weight_male             NUMERIC(10,2)  (in lb/kg)                  │
│  • weight_female           NUMERIC(10,2)  (in lb/kg)                  │
│  • calories               INTEGER                                  │
│  • is_max_effort          BOOLEAN  (e.g., "Max Wall Balls") │
│  • notes                  TEXT    (parsing notes)               │
│  • mini_circuit_id        INTEGER  (FK optional) → mini_circuits_staging.id │
│  • time_segment_id         INTEGER  (FK optional) → time_segments_staging.id │
│  • ladder_rung_id         INTEGER  (FK optional) → ladder_rungs_staging.id │
│  • created_at             TIMESTAMP                                     │
└───────────────────────────┬─────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               hyrox_mini_circuits_staging                            │
│  ──────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • circuit_number           INTEGER  (1, 2, 3...)              │
│  • circuit_type            ENUM     amrap/emom/for_time/...    │
│  • start_time              TIME     Start time of circuit (if explicit) │
│  • end_time                TIME     End time of circuit (if explicit)   │
│  • duration_minutes        INTEGER  Duration in minutes                │
│  • rest_after_minutes      INTEGER  Rest after circuit (minutes)    │
│  • notes                  TEXT    Circuit description/notes             │
└─────────────────────────────────────────────────────────────────────┘

                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               hyrox_time_segments_staging                           │
│  ──────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • segment_number           INTEGER  (1, 2, 3...)              │
│  • start_time              TIME     "0:00", "16:00"              │
│  • end_time                TIME     "15:00", "30:00"              │
│  • duration_minutes        INTEGER  Duration in minutes                │
│  • notes                  TEXT    Segment description/notes             │
└─────────────────────────────────────────────────────────────────────┘

                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 hyrox_ladder_rungs_staging                           │
│  ──────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • rung_number             INTEGER  (1, 2, 3...)              │
│  • reps_per_exercise      INTEGER  (e.g., 15-10-5 ladder)  │
│  • is_ascending            BOOLEAN  (climbing or descending)       │
│  • notes                  TEXT     (e.g., "descending reps")    │
└─────────────────────────────────────────────────────────────────────┘

                           │
                           │ FK: workout_id
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                hyrox_workout_tags_staging                             │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • tag_name               VARCHAR(100)                             │
│  • tag_url                TEXT    (optional URL to tag)          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Complete Column Definitions

### hyrox_workouts_staging (6 tables total)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `wod_id` | VARCHAR(100) | YES | Workout slug from URL (e.g., "beverly-hills") |
| `name` | VARCHAR(255) | NO | Workout name (e.g., "Beverly Hills") |
| `url` | TEXT | NO | Full URL to workout |
| `badge` | TEXT | YES | Badge text (e.g., "Hyrox Workout of Week") |
| `workout_type` | ENUM (hyrox_workout_type) | NO | 'unknown' | amrap, emom, for_time, rounds_for_time, for_load, buy_in, cash_out, time_cap, ladder, mini_circuit, explicit_time_guidance, unknown |
| `workout_goal` | ENUM (hyrox_workout_goal) | YES | 'unknown' | max_rounds_reps, finish_quickly, complete_rounds, max_load, pace_work, endurance, strength, mixed, unknown |
| `time_specification` | VARCHAR(100) | YES | Time spec text (e.g., "AMRAP in 25 minutes") |
| `total_time_minutes` | INTEGER | YES | Total workout time in minutes |
| `time_cap_minutes` | INTEGER | YES | Time cap in minutes (if any) |
| `has_buy_in` | BOOLEAN | NO | false | Workout has buy-in section |
| `has_cash_out` | BOOLEAN | NO | false | Workout has cash-out section |
| `is_complex` | BOOLEAN | NO | false | Has mini circuits, ladders, or time segments |
| `full_description` | TEXT | YES | Complete workout description text |
| `scraped_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | When workout was scraped |
| `source_page` | VARCHAR(100) | YES | Source page identifier |
| `status` | ENUM (hyrox_status) | NO | 'pending_review' | pending_review, reviewed, approved, rejected |
| `notes` | TEXT | YES | Manual notes or instructions |

**Indexes:**
- `idx_hyrox_workouts_staging_name` on `(name)`
- `idx_hyrox_workouts_staging_type` on `(workout_type)`
- `idx_hyrox_workouts_staging_status` on `(status)`
- `idx_hyrox_workouts_staging_scraped_at` on `(scraped_at)`

---

### hyrox_workout_lines_staging (Movement grain table - improved)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `line_number` | INTEGER | NO | 0-based sequence in workout |
| `line_text` | TEXT | NO | Original description line text |
| `is_rest` | BOOLEAN | NO | false | Is this a rest period? |
| `is_buy_in` | BOOLEAN | NO | false | Is this part of buy-in? |
| `is_cash_out` | BOOLEAN | NO | false | Is this part of cash-out? |
| `movement_name` | VARCHAR(200) | YES | Normalized movement name (e.g., "wall ball shots") |
| `reps` | INTEGER | YES | Number of repetitions |
| `distance_meters` | NUMERIC(10,2) | YES | Distance in meters |
| `duration_seconds` | INTEGER | YES | Duration in seconds |
| `weight_male` | NUMERIC(10,2) | YES | Male weight (lb/kg) |
| `weight_female` | NUMERIC(10,2) | YES | Female weight (lb/kg) |
| `calories` | INTEGER | YES | Calorie target |
| `is_max_effort` | BOOLEAN | NO | false | Is this a "max" effort (e.g., "Max Wall Balls")? |
| `notes` | TEXT | YES | Parsing notes or corrections |
| `mini_circuit_id` | INTEGER (FK) | YES | → hyrox_mini_circuits_staging.id (SET NULL) |
| `time_segment_id` | INTEGER (FK) | YES | → hyrox_time_segments_staging.id (SET NULL) |
| `ladder_rung_id` | INTEGER (FK) | YES | → hyrox_ladder_rungs_staging.id (SET NULL) |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_workout_lines_staging_workout` on `(workout_id)`
- `idx_hyrox_workout_lines_staging_movement` on `(movement_name)`
- `idx_hyrox_workout_lines_staging_circuit` on `(mini_circuit_id)`
- `idx_hyrox_workout_lines_staging_segment` on `(time_segment_id)`
- `idx_hyrox_workout_lines_staging_ladder` on `(ladder_rung_id)`

---

### hyrox_mini_circuits_staging (For workouts with multiple circuits)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `circuit_number` | INTEGER | NO | Circuit order (1, 2, 3...) |
| `circuit_type` | ENUM (hyrox_workout_type) | NO | Type of this circuit |
| `start_time` | TIME | YES | Start time (e.g., "00:00:00", "16:00:00") |
| `end_time` | TIME | YES | End time (e.g., "15:00:00", "30:00:00") |
| `duration_minutes` | INTEGER | YES | Duration in minutes |
| `rest_after_minutes` | INTEGER | YES | Rest after this circuit (in minutes) |
| `notes` | TEXT | YES | Circuit description/notes |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_mini_circuits_staging_workout` on `(workout_id)`

---

### hyrox_time_segments_staging (For explicit time guidance workouts)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `segment_number` | INTEGER | NO | Segment order (1, 2, 3...) |
| `start_time` | TIME | YES | Start time (e.g., "00:00:00", "16:00:00") |
| `end_time` | TIME | YES | End time (e.g., "15:00:00", "30:00:00") |
| `duration_minutes` | INTEGER | YES | Duration in minutes |
| `notes` | TEXT | YES | Segment description/notes |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_time_segments_staging_workout` on `(workout_id)`

---

### hyrox_ladder_rungs_staging (For ladder workouts)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `rung_number` | INTEGER | NO | Rung order (1, 2, 3...) |
| `reps_per_exercise` | INTEGER | YES | Reps at this rung (e.g., 15, 10, 5) |
| `is_ascending` | BOOLEAN | NO | true | True if reps increase, false if descending |
| `notes` | TEXT | YES | Description of ladder pattern |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_ladder_rungs_staging_workout` on `(workout_id)`

---

### hyrox_workout_tags_staging

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `tag_name` | VARCHAR(100) | NO | Tag name |
| `tag_url` | TEXT | YES | URL to tag page |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_workout_tags_staging_workout` on `(workout_id)`

---

### hyrox_scraping_log_staging (Audit log - optional)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `scrape_session_id` | VARCHAR(100) | NO | Unique session identifier |
| `started_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Scrape start time |
| `completed_at` | TIMESTAMP WITHOUT TIME ZONE | YES | Scrape completion time |
| `total_workouts_found` | INTEGER | NO | 0 | Total workouts found |
| `workouts_scraped` | INTEGER | NO | 0 | Workouts successfully scraped |
| `workouts_saved` | INTEGER | NO | 0 | Workouts saved to database |
| `errors_count` | INTEGER | NO | 0 | Number of errors |
| `has_errors` | BOOLEAN | NO | false | Were there any errors? |
| `error_summary` | TEXT | YES | Error messages |
| `user_agent` | TEXT | YES | User agent used for scraping |
| `notes` | TEXT | YES | Additional notes |

**Indexes:**
- `idx_hyrox_scraping_log_staging_session` on `(scrape_session_id)`

---

## Key Design Decisions

### 1. Why 6 tables instead of 8?

**Removed:**
- `hyrox_workout_movements_staging` - redundant with `hyrox_workout_lines_staging`
- `favorites_count`, `comments_count` - scraping artifacts, not core workout data

**Retained:**
- `hyrox_workouts_staging` - core workout metadata
- `hyrox_workout_lines_staging` - movement grain with FKs to structures
- `hyrox_mini_circuits_staging` - multi-circuit workouts
- `hyrox_time_segments_staging` - time-segmented workouts
- `hyrox_ladder_rungs_staging` - ladder workouts
- `hyrox_workout_tags_staging` - categorization

### 2. Foreign Keys in Lines Table

Instead of separate JSON arrays in structure tables, lines now have optional FKs:
- `mini_circuit_id` → links line to its circuit
- `time_segment_id` → links line to its time segment
- `ladder_rung_id` → links line to its ladder rung

**Benefits:**
- Direct SQL joins without JSON parsing
- Efficient filtering by circuit/segment/ladder
- Referential integrity

### 3. TIME instead of VARCHAR for time fields

**Before:** `start_time VARCHAR(50)` → "0:00"
**After:** `start_time TIME` → "00:00:00"

**Benefits:**
- Proper time type for comparisons and sorting
- Automatic validation
- Queryable with time functions

---

## How to Extract Full Workout for Program Builder

### SQL Query: Get Complete Workout with All Movements

```sql
WITH workout_details AS (
  SELECT
    w.id,
    w.name,
    w.workout_type,
    w.workout_goal,
    w.total_time_minutes,
    w.time_cap_minutes,
    w.has_buy_in,
    w.has_cash_out,
    w.is_complex,
    w.full_description,
    w.notes
  FROM hyrox_workouts_staging w
  WHERE w.id = $workout_id
),
ordered_lines AS (
  SELECT
    l.line_number,
    l.line_text,
    l.is_rest,
    l.is_buy_in,
    l.is_cash_out,
    l.movement_name,
    l.reps,
    l.distance_meters,
    l.duration_seconds,
    l.weight_male,
    l.weight_female,
    l.calories,
    l.is_max_effort,
    l.mini_circuit_id,
    l.time_segment_id,
    l.ladder_rung_id,
    mc.circuit_number,
    ts.segment_number,
    lr.rung_number
  FROM hyrox_workout_lines_staging l
  LEFT JOIN hyrox_mini_circuits_staging mc ON l.mini_circuit_id = mc.id
  LEFT JOIN hyrox_time_segments_staging ts ON l.time_segment_id = ts.id
  LEFT JOIN hyrox_ladder_rungs_staging lr ON l.ladder_rung_id = lr.id
  WHERE l.workout_id = $workout_id
  ORDER BY l.line_number
),
structured_sections AS (
  SELECT
    mc.id as mini_circuit_id,
    mc.circuit_number,
    mc.circuit_type,
    mc.start_time,
    mc.end_time,
    mc.duration_minutes,
    mc.rest_after_minutes,
    mc.notes
  FROM hyrox_mini_circuits_staging mc
  WHERE mc.workout_id = $workout_id
),
time_segment_sections AS (
  SELECT
    ts.id as time_segment_id,
    ts.segment_number,
    ts.start_time,
    ts.end_time,
    ts.duration_minutes,
    ts.notes
  FROM hyrox_time_segments_staging ts
  WHERE ts.workout_id = $workout_id
)
SELECT
  wd.*,
  json_agg(json_build_object(
    'line_number', ol.line_number,
    'text', ol.line_text,
    'is_rest', ol.is_rest,
    'is_buy_in', ol.is_buy_in,
    'is_cash_out', ol.is_cash_out,
    'movement', ol.movement_name,
    'reps', ol.reps,
    'distance_meters', ol.distance_meters,
    'duration_seconds', ol.duration_seconds,
    'weight_male', ol.weight_male,
    'weight_female', ol.weight_female,
    'calories', ol.calories,
    'is_max_effort', ol.is_max_effort,
    'mini_circuit_number', ol.circuit_number,
    'time_segment_number', ol.segment_number,
    'ladder_rung_number', ol.rung_number
  ) ORDER BY ol.line_number) as movements,
  json_agg(json_build_object(
    'circuit_number', sc.circuit_number,
    'circuit_type', sc.circuit_type,
    'start_time', sc.start_time,
    'end_time', sc.end_time,
    'duration_minutes', sc.duration_minutes,
    'rest_after_minutes', sc.rest_after_minutes,
    'notes', sc.notes
  ) ORDER BY sc.circuit_number) as mini_circuits,
  json_agg(json_build_object(
    'segment_number', tss.segment_number,
    'start_time', tss.start_time,
    'end_time', tss.end_time,
    'duration_minutes', tss.duration_minutes,
    'notes', tss.notes
  ) ORDER BY tss.segment_number) as time_segments
FROM workout_details wd
CROSS JOIN ordered_lines ol ON true
LEFT JOIN structured_sections sc ON sc.mini_circuit_id IS NOT NULL
LEFT JOIN time_segment_sections tss ON tss.time_segment_id IS NOT NULL
GROUP BY wd.id;
```

---

## Comparison: Original vs Refined

| Aspect | Original (8 tables) | Refined (6 tables) |
|---------|---------------------|-------------------|
| Total tables | 8 | 6 |
| Scraping artifacts | favorites_count, comments_count | Removed |
| Redundant table | hyrox_workout_movements_staging | Removed |
| Time fields | VARCHAR(50) | TIME type |
| JSON arrays | In structure tables | FK relationships in lines |
| Core tables | 6 essential | 6 essential |

---

## Conclusion

The refined schema:
- **Removes 2 unnecessary tables** (movements_staging, scraping artifacts)
- **Improves data types** (TIME instead of VARCHAR for time fields)
- **Simplifies queries** (FKs instead of JSON parsing)
- **Maintains all functionality** (complete workout reconstruction)
- **Better for program builder** (direct joins, proper types)

**Recommendation:** Proceed with refined 6-table design.
