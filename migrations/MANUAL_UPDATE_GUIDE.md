# Manual Movements Update Guide

## Overview
This guide provides a safe workflow for making manual updates to the movements table columns.

## Target Columns
- primary_region (ENUM, required)
- bodyweight_possible (BOOLEAN, nullable)
- dumbbell_possible (BOOLEAN, nullable)
- kettlebell_possible (BOOLEAN, nullable)
- barbell_possible (BOOLEAN, nullable)
- machine_possible (BOOLEAN, nullable)
- band_possible (BOOLEAN, nullable)
- plate_or_med_ball_possible (BOOLEAN, nullable)
- pattern (ENUM, nullable)
- pattern_subtype (ENUM, nullable)

## Acceptable Values

### 1. primary_region (ENUM - Required)
**Type**: primaryregion enum
**Constraint**: NOT NULL

**Valid Values**:
- anterior_lower
- anterior_upper
- posterior_lower
- posterior_upper
- shoulder
- core
- full_body
- lower_body
- upper_body

**Current Data**: 9 distinct values in use

### 2-8. Equipment Columns (BOOLEAN - Nullable)
**Type**: boolean
**Default**: false
**Constraint**: Nullable

**Valid Values**:
- true (movement can be performed with this equipment)
- false (movement cannot be performed with this equipment)
- NULL (unknown/not specified)

**Columns**:
- bodyweight_possible
- dumbbell_possible
- kettlebell_possible
- barbell_possible
- machine_possible
- band_possible
- plate_or_med_ball_possible

### 9. pattern (ENUM - Nullable)
**Type**: pattern enum
**Constraint**: Nullable

**Valid Values** (31 total):
- squat, hinge, lunge
- push, pull, carry, twist, crawl, jump, throw, grip, core
- upper_push, upper_pull, lower_push, lower_pull
- full_body, cardio, mobility, other
- horizontal_push, horizontal_pull
- stretch, conditioning, plyometric
- vertical_push, vertical_pull, olympic, isometric, rotation

**Current Data**: 9 distinct values in use:
- squat, hinge, lunge, carry, rotation
- horizontal_push, horizontal_pull
- vertical_push, vertical_pull

### 10. pattern_subtype (ENUM - Nullable)
**Type**: pattern_subtype enum
**Constraint**: Nullable

**Valid Values** (36 total):
- squat, hinge, lunge
- horizontal_push, horizontal_pull
- vertical_push, vertical_pull, rotation, carry
- plyometric, isometric
- run, row, bike, cycle, swim, elliptical
- sled_push, sled_pull, sled_drag
- burpee, turkish_get_up
- farmer_carry, waiter_carry, suitcase_carry
- bear_crawl, crab_walk
- mobility, stretch, activation
- dynamic_warmup, static_stretch, foam_roll
- anti_extension, anti_rotation, anti_lateral_flexion

**Current Data**: 24 distinct values in use

## Safe Update Workflow

### Step 1: Create Backup (BEFORE any changes)
```bash
docker cp /Users/shourjosmac/Documents/Alloy\ V0/migrations/20260228_pre_update_backup.sql 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454:/docker-entrypoint-initdb.d/20260228_pre_update_backup.sql && docker exec -it 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454 psql -U jacked -d Jacked-DB -f /docker-entrypoint-initdb.d/20260228_pre_update_backup.sql
```

**Expected Output**: Should show "Backup created successfully: 524 rows backed up"

### Step 2: Verify Backup
```bash
docker exec -it 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454 psql -U jacked -d Jacked-DB -c "SELECT COUNT(*) as backup_count FROM movements_backup_20260228;"
```

**Expected**: 524 rows

### Step 3: Make Manual Updates
Use SQL UPDATE statements to modify values. Examples:

```sql
-- Update primary region for specific movements
UPDATE movements SET primary_region = 'posterior_upper' WHERE name = 'Deadlift';

-- Update equipment possibilities
UPDATE movements SET barbell_possible = true WHERE name = 'Bench Press';

-- Update pattern
UPDATE movements SET pattern = 'horizontal_push' WHERE name = 'Push-up';

-- Update pattern subtype
UPDATE movements SET pattern_subtype = 'horizontal_push' WHERE name = 'Bench Press';
```

### Step 4: Run Validation (AFTER all changes)
```bash
docker cp /Users/shourjosmac/Documents/Alloy\ V0/migrations/20260228_post_update_validation.sql 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454:/docker-entrypoint-initdb.d/20260228_post_update_validation.sql && docker exec -it 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454 psql -U jacked -d Jacked-DB -f /docker-entrypoint-initdb.d/20260228_post_update_validation.sql
```

**Check for**: 
- WARNING messages in the output
- Any non-zero values in "failed_count" columns
- All validation checks should PASS

### Step 5: Review Changes (Optional but Recommended)
```bash
# See which rows changed for primary_region
docker exec -it 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454 psql -U jacked -d Jacked-DB -c "SELECT m.id, m.name, m.primary_region as new_value, b.primary_region as old_value FROM movements m JOIN movements_backup_20260228 b ON m.id = b.id WHERE m.primary_region IS DISTINCT FROM b.primary_region LIMIT 10;"
```

## Rollback Procedure

If validation fails or you need to undo changes:

```bash
docker cp /Users/shourjosmac/Documents/Alloy\ V0/migrations/20260228_rollback.sql 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454:/docker-entrypoint-initdb.d/20260228_rollback.sql && docker exec -it 43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454 psql -U jacked -d Jacked-DB -f /docker-entrypoint-initdb.d/20260228_rollback.sql
```

**Expected Output**: "Rollback completed: 524 rows restored from backup"

## Important Notes

1. **Never skip the backup step** - it's your safety net
2. **Run validation after updates** - catch errors before they propagate
3. **Test with a single row first** - verify your UPDATE statement works as expected
4. **Keep track of your changes** - document what you modified and why
5. **Enum values are case-sensitive** - use exact values from the lists above
6. **NULL is valid for nullable columns** - use it when a value is truly unknown
7. **Boolean columns** - use true/false, not TRUE/FALSE or 1/0

## Common Queries for Reference

```sql
-- Check current distinct values for any column
SELECT DISTINCT primary_region, COUNT(*) FROM movements GROUP BY primary_region ORDER BY primary_region;

-- Find movements with no equipment set (all false)
SELECT id, name FROM movements WHERE 
    bodyweight_possible = false AND
    dumbbell_possible = false AND
    kettlebell_possible = false AND
    barbell_possible = false AND
    machine_possible = false AND
    band_possible = false AND
    plate_or_med_ball_possible = false;

-- Count movements by pattern
SELECT pattern, COUNT(*) FROM movements GROUP BY pattern ORDER BY COUNT(*) DESC;
```

## Script Files

1. **20260228_pre_update_backup.sql** - Creates backup table
2. **20260228_post_update_validation.sql** - Validates changes
3. **20260228_rollback.sql** - Restores from backup

All scripts are idempotent and can be re-run safely.
