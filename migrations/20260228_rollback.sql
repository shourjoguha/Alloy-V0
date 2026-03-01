-- Migration: 20260228_rollback
-- Purpose: Restore movements table columns to pre-update state from backup
-- Run this ONLY if you need to rollback manual changes
-- REQUIRES: movements_backup_20260228 table to exist (created by pre_update_backup.sql)

BEGIN;

-- Verify backup exists
DO $$
DECLARE
    backup_exists BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_name = 'movements_backup_20260228'
    ) INTO backup_exists;
    
    IF NOT backup_exists THEN
        RAISE EXCEPTION 'Backup table movements_backup_20260228 does not exist. Cannot rollback!';
    END IF;
    
    RAISE NOTICE 'Backup table found. Proceeding with rollback...';
END $$;

-- Restore columns from backup
UPDATE movements m
SET 
    primary_region = b.primary_region,
    bodyweight_possible = b.bodyweight_possible,
    dumbbell_possible = b.dumbbell_possible,
    kettlebell_possible = b.kettlebell_possible,
    barbell_possible = b.barbell_possible,
    machine_possible = b.machine_possible,
    band_possible = b.band_possible,
    plate_or_med_ball_possible = b.plate_or_med_ball_possible,
    pattern = b.pattern,
    pattern_subtype = b.pattern_subtype
FROM movements_backup_20260228 b
WHERE m.id = b.id;

-- Log rollback summary
DO $$
DECLARE
    rollback_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO rollback_count FROM movements_backup_20260228;
    RAISE NOTICE 'Rollback completed: % rows restored from backup', rollback_count;
    RAISE NOTICE 'Target columns restored: primary_region, bodyweight_possible, dumbbell_possible, kettlebell_possible, barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible, pattern, pattern_subtype';
END $$;

COMMIT;

-- Verification query (run after this script to confirm rollback):
-- SELECT m.id, m.name, m.primary_region as current_region, b.primary_region as backup_region 
-- FROM movements m 
-- JOIN movements_backup_20260228 b ON m.id = b.id 
-- WHERE m.primary_region IS DISTINCT FROM b.primary_region
-- LIMIT 10;
-- 
-- Should return 0 rows if rollback was successful
