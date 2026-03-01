# Hyrox Staging Schema Design

## Overview
The Hyrox staging schema uses a grain of **individual movements and rest blocks** that make up a Hyrox workout. This allows complete reconstruction of workouts for program builders.

---

## Schema Visualization

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    hyrox_workouts_staging                         │
│  ──────────────────────────────────────────────────────────────     │
│  • id (PK)           INTEGER  AUTO_INCREMENT                   │
│  • wod_id             VARCHAR(100)   URL slug                    │
│  • name               VARCHAR(255)   Workout name                │
│  • workout_type       ENUM           amrap/emom/for_time/...    │
│  • workout_goal       ENUM           max_rounds/finish_quickly  │
│  • total_time_minutes INTEGER                                              │
│  • time_cap_minutes   INTEGER                                              │
│  • has_buy_in        BOOLEAN                                              │
│  • has_cash_out      BOOLEAN                                              │
│  • is_complex        BOOLEAN    Mini circuits/ladders/time segments │
│  • source_page        VARCHAR(100)                                           │
│  • scraped_at        TIMESTAMP                                             │
│  • status            ENUM           pending_review/reviewed/...    │
└───────────────────────────┬─────────────────────────────────────────────┘
                           │ FK: workout_id
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 hyrox_workout_lines_staging                         │
│  ──────────────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • line_number              INTEGER  (sequence in workout)       │
│  • line_text                TEXT    (original description)       │
│  • is_rest                 BOOLEAN                                  │
│  • is_buy_in              BOOLEAN                                  │
│  • is_cash_out             BOOLEAN                                  │
│  • movement_name           VARCHAR(200)  (normalized name)    │
│  • metric_type             VARCHAR(50)  (reps/distance/...) │
│  • metric_unit             VARCHAR(20)  (m/seconds/...)    │
│  • reps                    INTEGER                                  │
│  • distance_meters         NUMERIC                                  │
│  • duration_seconds        INTEGER                                  │
│  • weight_male             NUMERIC  (in lb/kg)                  │
│  • weight_female           NUMERIC  (in lb/kg)                  │
│  • calories               INTEGER                                  │
│  • is_max_effort          BOOLEAN  (e.g., "Max Wall Balls") │
│  • notes                  TEXT    (parsing notes)               │
└───────────────────────────┬─────────────────────────────────────────────┘
                           │
                           │ FK: mini_circuit_id (optional)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               hyrox_mini_circuits_staging                            │
│  ──────────────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • circuit_number           INTEGER  (1, 2, 3...)              │
│  • circuit_type            ENUM     amrap/emom/for_time/...    │
│  • time_specification      VARCHAR(100)  "AMRAP in 25 min"   │
│  • rest_after_seconds      INTEGER  (rest between circuits)       │
│  • total_time_seconds     INTEGER  (circuit duration)          │
└─────────────────────────────────────────────────────────────────────┘

                           │
                           │ FK: time_segment_id (optional)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               hyrox_time_segments_staging                           │
│  ──────────────────────────────────────────────────────────────     │
│  • id (PK)                INTEGER  AUTO_INCREMENT              │
│  • workout_id (FK)          INTEGER  → hyrox_workouts_staging.id │
│  • segment_number           INTEGER  (1, 2, 3...)              │
│  • start_time              VARCHAR(50)  "0:00", "16:00"      │
│  • end_time                VARCHAR(50)  "15:00", "30:00"      │
│  • duration_minutes        INTEGER                                  │
│  • movements              JSONB    (array of line_ids)         │
└─────────────────────────────────────────────────────────────────────┘

                           │
                           │ FK: ladder_id (optional)
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 hyrox_ladder_rungs_staging                           │
│  ──────────────────────────────────────────────────────────────     │
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

### hyrox_workouts_staging (Main workout table)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-----------|-------------|
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
| `background_image` | TEXT | YES | URL to background image |
| `favorites_count` | INTEGER | NO | 0 | Number of favorites |
| `comments_count` | INTEGER | NO | 0 | Number of comments |
| `full_description` | TEXT | YES | Complete workout description text |
| `scraped_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | When workout was scraped |
| `source_page` | VARCHAR(100) | YES | Source page identifier |
| `status` | ENUM (hyrox_status) | NO | 'pending_review' | pending_review, reviewed, approved, rejected |
| `validation_errors` | JSONB | YES | JSON array of validation errors |
| `notes` | TEXT | YES | Manual notes about the workout |

**Indexes:**
- `idx_hyrox_workouts_staging_name` on `(name)`
- `idx_hyrox_workouts_staging_type` on `(workout_type)`
- `idx_hyrox_workouts_staging_status` on `(status)`
- `idx_hyrox_workouts_staging_scraped_at` on `(scraped_at)`

---

### hyrox_workout_lines_staging (Movement grain table)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `line_number` | INTEGER | NO | 0-based sequence in workout |
| `line_text` | TEXT | NO | Original description line text |
| `is_rest` | BOOLEAN | NO | false | Is this a rest period? |
| `is_buy_in` | BOOLEAN | NO | false | Is this part of buy-in? |
| `is_cash_out` | BOOLEAN | NO | false | Is this part of cash-out? |
| `movement_name` | VARCHAR(200) | YES | Normalized movement name (e.g., "wall ball shots") |
| `metric_type` | VARCHAR(50) | YES | Type: 'reps', 'distance', 'duration', 'weight', 'calories', 'max_effort' |
| `metric_unit` | VARCHAR(20) | YES | Unit: 'count', 'meters', 'seconds', 'lb', 'kg', 'calories' |
| `reps` | INTEGER | YES | Number of repetitions |
| `distance_meters` | NUMERIC(10, 2) | YES | Distance in meters |
| `duration_seconds` | INTEGER | YES | Duration in seconds |
| `weight_male` | NUMERIC(10, 2) | YES | Male weight (lb/kg) |
| `weight_female` | NUMERIC(10, 2) | YES | Female weight (lb/kg) |
| `calories` | INTEGER | YES | Calorie target |
| `is_max_effort` | BOOLEAN | NO | false | Is this a "max" effort (e.g., "Max Wall Balls")? |
| `notes` | TEXT | YES | Parsing notes or corrections |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_workout_lines_staging_workout` on `(workout_id)`
- `idx_hyrox_workout_lines_staging_movement` on `(movement_name)`
- `idx_hyrox_workout_lines_staging_type` on `(metric_type)`

---

### hyrox_mini_circuits_staging (For workouts with multiple circuits)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `circuit_number` | INTEGER | NO | Circuit order (1, 2, 3...) |
| `circuit_type` | ENUM (hyrox_workout_type) | NO | Type of this circuit |
| `time_specification` | VARCHAR(100) | YES | Time spec (e.g., "AMRAP in 25 min") |
| `rest_after_seconds` | INTEGER | YES | Rest after this circuit |
| `total_time_seconds` | INTEGER | YES | Total duration of circuit |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_mini_circuits_staging_workout` on `(workout_id)`

---

### hyrox_time_segments_staging (For explicit time guidance workouts)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `segment_number` | INTEGER | NO | Segment order (1, 2, 3...) |
| `start_time` | VARCHAR(50) | YES | Start time (e.g., "0:00", "16:00") |
| `end_time` | VARCHAR(50) | YES | End time (e.g., "15:00", "30:00") |
| `duration_minutes` | INTEGER | YES | Duration in minutes |
| `movements` | JSONB | YES | Array of line_ids in this segment |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_time_segments_staging_workout` on `(workout_id)`

---

### hyrox_ladder_rungs_staging (For ladder workouts)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-----------|-------------|
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
|---------|--------|-----------|-----------|-------------|
| `id` | INTEGER (PK, GENERATED BY DEFAULT AS IDENTITY) | NO | Auto-increment ID |
| `workout_id` | INTEGER (FK) | NO | → hyrox_workouts_staging.id (CASCADE DELETE) |
| `tag_name` | VARCHAR(100) | NO | Tag name |
| `tag_url` | TEXT | YES | URL to tag page |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NO | NOW() | Record creation time |

**Indexes:**
- `idx_hyrox_workout_tags_staging_workout` on `(workout_id)`

---

### hyrox_scraping_log_staging (Audit log)

| Column | Type | Nullable | Default | Description |
|---------|--------|-----------|-----------|-------------|
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
    w.full_description
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
    l.metric_type,
    l.metric_unit,
    l.reps,
    l.distance_meters,
    l.duration_seconds,
    l.weight_male,
    l.weight_female,
    l.calories,
    l.is_max_effort
  FROM hyrox_workout_lines_staging l
  WHERE l.workout_id = $workout_id
  ORDER BY l.line_number
),
mini_circuits AS (
  SELECT
    mc.circuit_number,
    mc.circuit_type,
    mc.time_specification,
    mc.rest_after_seconds,
    mc.total_time_seconds
  FROM hyrox_mini_circuits_staging mc
  WHERE mc.workout_id = $workout_id
  ORDER BY mc.circuit_number
),
time_segments AS (
  SELECT
    ts.segment_number,
    ts.start_time,
    ts.end_time,
    ts.duration_minutes
  FROM hyrox_time_segments_staging ts
  WHERE ts.workout_id = $workout_id
  ORDER BY ts.segment_number
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
    'metric_type', ol.metric_type,
    'metric_unit', ol.metric_unit,
    'reps', ol.reps,
    'distance_meters', ol.distance_meters,
    'duration_seconds', ol.duration_seconds,
    'weight_male', ol.weight_male,
    'weight_female', ol.weight_female,
    'calories', ol.calories,
    'is_max_effort', ol.is_max_effort
  ) ORDER BY ol.line_number) as movements,
  json_agg(json_build_object(
    'circuit_number', mc.circuit_number,
    'circuit_type', mc.circuit_type,
    'time_specification', mc.time_specification,
    'rest_after_seconds', mc.rest_after_seconds,
    'total_time_seconds', mc.total_time_seconds
  ) ORDER BY mc.circuit_number) as mini_circuits,
  json_agg(json_build_object(
    'segment_number', ts.segment_number,
    'start_time', ts.start_time,
    'end_time', ts.end_time,
    'duration_minutes', ts.duration_minutes
  ) ORDER BY ts.segment_number) as time_segments
FROM workout_details wd
CROSS JOIN ordered_lines ol ON true
LEFT JOIN mini_circuits mc ON mc.workout_id = wd.id
LEFT JOIN time_segments ts ON ts.workout_id = wd.id
GROUP BY wd.id;
```

### Example Output JSON Structure

```json
{
  "id": 9,
  "name": "Beverly Hills",
  "workout_type": "amrap",
  "workout_goal": "complete_rounds",
  "total_time_minutes": 25,
  "time_cap_minutes": null,
  "has_buy_in": false,
  "has_cash_out": false,
  "is_complex": false,
  "full_description": "AMRAP in 25 minutes\nComplete 5 rounds of:\n...",
  "movements": [
    {
      "line_number": 0,
      "text": "AMRAP in 25 minutes",
      "is_rest": false,
      "is_buy_in": false,
      "is_cash_out": false,
      "movement": null,
      "metric_type": null,
      "metric_unit": null,
      "reps": null,
      "distance_meters": null,
      "duration_seconds": null,
      "weight_male": null,
      "weight_female": null,
      "calories": null,
      "is_max_effort": false
    },
    {
      "line_number": 1,
      "text": "Complete 5 rounds of:",
      "is_rest": false,
      "is_buy_in": false,
      "is_cash_out": false,
      "movement": null,
      "metric_type": null,
      "metric_unit": null,
      "reps": null,
      "distance_meters": null,
      "duration_seconds": null,
      "weight_male": null,
      "weight_female": null,
      "calories": null,
      "is_max_effort": false
    },
    {
      "line_number": 2,
      "text": "40 second Max Wall Ball Shots (20/14 lb)",
      "is_rest": false,
      "is_buy_in": false,
      "is_cash_out": false,
      "movement": "wall ball shots",
      "metric_type": "duration",
      "metric_unit": "seconds",
      "reps": null,
      "distance_meters": null,
      "duration_seconds": 40,
      "weight_male": 20,
      "weight_female": 14,
      "calories": null,
      "is_max_effort": true
    },
    {
      "line_number": 3,
      "text": "20 second Rest",
      "is_rest": true,
      "is_buy_in": false,
      "is_cash_out": false,
      "movement": null,
      "metric_type": "duration",
      "metric_unit": "seconds",
      "reps": null,
      "distance_meters": null,
      "duration_seconds": 20,
      "weight_male": null,
      "weight_female": null,
      "calories": null,
      "is_max_effort": false
    }
  ],
  "mini_circuits": [],
  "time_segments": []
}
```

---

## Metric Types Reference

| metric_type | metric_unit | Example |
|-------------|---------------|----------|
| `reps` | `count` | 20 Burpees |
| `distance` | `meters` | 400 meter Run |
| `duration` | `seconds` | 40 second Max... |
| `duration` | `minutes` | 25 minutes |
| `weight` | `lb` | 20 lb |
| `weight` | `kg` | 9 kg |
| `calories` | `calories` | 15 calorie Row |
| `max_effort` | `null` | Max Wall Ball Shots |

---

## Weight Parsing Logic

Weights in Hyrox workouts are typically specified as dual weights:
- Example: `(20/14 lb)` = 20 lb male, 14 lb female
- Example: `(9/6 kg)` = 9 kg male, 6 kg female
- Example: `(60/40 lb)` = 60 lb male, 40 lb female

Parsing regex:
```python
weight_pattern = r'\((\d+)/(\d+)\s*(lb|kg)\)'
weight_male = group1 (as numeric)
weight_female = group2 (as numeric)
weight_unit = group3 (lb or kg)
```

---

## Complex Workout Detection

A workout is marked `is_complex = true` if it contains:
- Mini circuits (multiple AMRAP/EMOM sections with rest between)
- Time segments (explicit time guidance like "0:00-15:00, 16:00-30:00")
- Ladders (ascending/descending reps)
- Buy-in/Cash-out (workouts with distinct sections)

---

## Quick Search Queries

### Find all AMRAP workouts
```sql
SELECT * FROM hyrox_workouts_staging
WHERE workout_type = 'amrap'
ORDER BY scraped_at DESC;
```

### Find workouts by movement
```sql
SELECT DISTINCT w.*
FROM hyrox_workouts_staging w
JOIN hyrox_workout_lines_staging l ON w.id = l.workout_id
WHERE l.movement_name = 'wall ball shots'
ORDER BY w.scraped_at DESC;
```

### Find workouts under 30 minutes
```sql
SELECT * FROM hyrox_workouts_staging
WHERE total_time_minutes < 30
ORDER BY total_time_minutes;
```

### Find workouts with buy-in
```sql
SELECT * FROM hyrox_workouts_staging
WHERE has_buy_in = true;
```

### Get workout summary by type
```sql
SELECT
  workout_type,
  COUNT(*) as count,
  AVG(total_time_minutes) as avg_duration
FROM hyrox_workouts_staging
WHERE total_time_minutes IS NOT NULL
GROUP BY workout_type
ORDER BY count DESC;
```

---

## Data Quality Validation Rules

1. **Required fields**: Every workout must have `name`, `url`, `workout_type`
2. **Movement lines**: Every workout must have at least 1 movement line
3. **Metric consistency**: If `metric_type` is 'reps', then `reps` must not be null
4. **Weight validation**: If `weight_male` exists, `weight_female` must exist (dual weights)
5. **Sequence integrity**: `line_number` must be sequential starting from 0
6. **Complex flag**: If `is_complex = true`, corresponding mini_circuits or time_segments records must exist
