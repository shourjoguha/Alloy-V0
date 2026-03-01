-- Migration: 20260228_pre_update_backup
-- Purpose: Create backup of movements table before manual column updates
-- Run this BEFORE making any manual changes to the target columns

BEGIN;

-- Create backup table with all current values
CREATE TABLE IF NOT EXISTS movements_backup_20260228 AS
SELECT 
    id,
    name,
    primary_region,
    bodyweight_possible,
    dumbbell_possible,
    kettlebell_possible,
    barbell_possible,
    machine_possible,
    band_possible,
    plate_or_med_ball_possible,
    pattern,
    pattern_subtype,
    NOW() as backup_timestamp
FROM movements;

-- Add primary key for better query performance
ALTER TABLE movements_backup_20260228 ADD PRIMARY KEY (id);

-- Add comment for documentation
COMMENT ON TABLE movements_backup_20260228 IS 'Backup of movements table before manual updates on 2026-02-28. Contains 11 target columns for rollback capability.';

-- Create index for faster rollback operations
CREATE INDEX IF NOT EXISTS idx_movements_backup_20260228_id ON movements_backup_20260228(id);

-- Log backup summary
DO $$
DECLARE
    backup_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO backup_count FROM movements_backup_20260228;
    RAISE NOTICE 'Backup created successfully: % rows backed up to movements_backup_20260228', backup_count;
END $$;

COMMIT;

-- Verification query (run after this script to confirm backup):
-- SELECT COUNT(*) as backup_count, MIN(backup_timestamp) as oldest_backup, MAX(backup_timestamp) as newest_backup FROM movements_backup_20260228;
