-- Migration: 20260228_add_core_conditioning_mobility_patterns
-- Description: Add new patterns (core, conditioning, mobility) and pattern_subtypes, and update movement data
-- ==== UP ====

-- Step 1: Alter patterntype_new enum to add new pattern values (each in separate transaction)
ALTER TYPE patterntype_new ADD VALUE IF NOT EXISTS 'core' AFTER 'rotation';
ALTER TYPE patterntype_new ADD VALUE IF NOT EXISTS 'conditioning' AFTER 'core';
ALTER TYPE patterntype_new ADD VALUE IF NOT EXISTS 'mobility' AFTER 'conditioning';

-- Step 2: Alter pattern_subtype enum to add new subtype values (each in separate transaction)
ALTER TYPE pattern_subtype ADD VALUE IF NOT EXISTS 'core' AFTER 'carry';
ALTER TYPE pattern_subtype ADD VALUE IF NOT EXISTS 'conditioning' AFTER 'foam_roll';
ALTER TYPE pattern_subtype ADD VALUE IF NOT EXISTS 'smr' AFTER 'anti_lateral_flexion';

-- Step 3: Now update movement data in a transaction
BEGIN;

-- Update movements with Crunch/Sit Up variants to core pattern/subtype
UPDATE movements
SET pattern = 'core', pattern_subtype = 'core'
WHERE LOWER(name) LIKE '%crunch%' 
   OR LOWER(name) LIKE '%sit up%'
   OR LOWER(name) LIKE '%sit-ups%'
   OR LOWER(name) LIKE '%situps%';

-- Update movements with smr/Cars/circles to mobility pattern/subtype
-- First update smr movements to use smr subtype
UPDATE movements
SET pattern_subtype = 'smr'
WHERE LOWER(name) LIKE '%smr%';

-- Then update circles and cars to mobility
UPDATE movements
SET pattern = 'mobility', pattern_subtype = 'mobility'
WHERE (LOWER(name) LIKE '%cars%' OR LOWER(name) LIKE '%circles%')
  AND pattern_subtype != 'smr';

-- Analyze and identify movements that should be conditioning pattern
-- Look for movements with cardio discipline that don't have a pattern yet
UPDATE movements
SET pattern = 'conditioning', pattern_subtype = 'conditioning'
WHERE discipline IN ('cardio', 'crossfit', 'athletic')
  AND pattern IS NULL;

-- Update remaining mobility-related movements
UPDATE movements
SET pattern = 'mobility', pattern_subtype = 'mobility'
WHERE discipline IN ('mobility', 'stretch')
  AND pattern IS NULL;

-- Verify and log changes
-- Count movements updated to core
DO $$
DECLARE
    core_count INTEGER;
    mobility_count INTEGER;
    conditioning_count INTEGER;
    smr_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO core_count FROM movements WHERE pattern = 'core';
    SELECT COUNT(*) INTO mobility_count FROM movements WHERE pattern = 'mobility';
    SELECT COUNT(*) INTO conditioning_count FROM movements WHERE pattern = 'conditioning';
    SELECT COUNT(*) INTO smr_count FROM movements WHERE pattern_subtype = 'smr';
    
    RAISE NOTICE 'Core movements: %', core_count;
    RAISE NOTICE 'Mobility movements: %', mobility_count;
    RAISE NOTICE 'Conditioning movements: %', conditioning_count;
    RAISE NOTICE 'SMR movements: %', smr_count;
END $$;

COMMIT;

-- ==== DOWN ====
BEGIN;

-- Note: Cannot drop enum values in PostgreSQL without recreating the type
-- This is a limitation of PostgreSQL's enum system
-- The rollback will only revert the data updates, not the enum additions

-- Rollback core pattern updates
UPDATE movements
SET pattern = 'carry', pattern_subtype = 'rotation'
WHERE pattern = 'core' AND (LOWER(name) LIKE '%jackknife%' OR LOWER(name) LIKE '%ghd%');

UPDATE movements
SET pattern = 'carry', pattern_subtype = 'carry'
WHERE pattern = 'core' AND (
    LOWER(name) LIKE '%sit up%' OR 
    LOWER(name) LIKE '%crunch%'
);

-- Rollback mobility pattern updates for circles/cars
UPDATE movements
SET pattern = CASE 
    WHEN LOWER(name) LIKE '%piriformis%' OR LOWER(name) LIKE '%hamstring%' OR 
         LOWER(name) LIKE '%lower back%' OR LOWER(name) LIKE '%iliotibial%' THEN 'hinge'::patterntype_new
    WHEN LOWER(name) LIKE '%quadriceps%' THEN 'squat'::patterntype_new
    WHEN LOWER(name) LIKE '%brachialis%' OR LOWER(name) LIKE '%latissimus%' OR 
         LOWER(name) LIKE '%rhomboids%' THEN 'horizontal_pull'::patterntype_new
    WHEN LOWER(name) LIKE '%knee%' OR LOWER(name) LIKE '%neck%' OR 
         LOWER(name) LIKE '%calves%' OR LOWER(name) LIKE '%foot%' OR 
         LOWER(name) LIKE '%arm%' OR LOWER(name) LIKE '%hip%' THEN 'carry'::patterntype_new
    WHEN LOWER(name) LIKE '%shoulder%' THEN 'vertical_push'::patterntype_new
    ELSE 'carry'::patterntype_new
END,
pattern_subtype = CASE 
    WHEN LOWER(name) LIKE '%piriformis%' OR LOWER(name) LIKE '%hamstring%' OR 
         LOWER(name) LIKE '%lower back%' OR LOWER(name) LIKE '%iliotibial%' THEN 'hinge'::pattern_subtype
    WHEN LOWER(name) LIKE '%quadriceps%' THEN 'squat'::pattern_subtype
    WHEN LOWER(name) LIKE '%brachialis%' OR LOWER(name) LIKE '%latissimus%' OR 
         LOWER(name) LIKE '%rhomboids%' THEN 'horizontal_pull'::pattern_subtype
    WHEN LOWER(name) LIKE '%knee%' OR LOWER(name) LIKE '%neck%' OR 
         LOWER(name) LIKE '%calves%' OR LOWER(name) LIKE '%foot%' OR 
         LOWER(name) LIKE '%arm%' OR LOWER(name) LIKE '%hip%' THEN 
        CASE 
            WHEN LOWER(name) LIKE '%knee%' THEN 'activation'::pattern_subtype
            WHEN LOWER(name) LIKE '%neck%' THEN 'activation'::pattern_subtype
            WHEN LOWER(name) LIKE '%calves%' THEN 'activation'::pattern_subtype
            WHEN LOWER(name) LIKE '%foot%' THEN 'activation'::pattern_subtype
            ELSE 'carry'::pattern_subtype
        END
    WHEN LOWER(name) LIKE '%shoulder%' THEN 'vertical_push'::pattern_subtype
    WHEN LOWER(name) LIKE '%hip%' THEN 'rotation'::pattern_subtype
    ELSE 'carry'::pattern_subtype
END
WHERE pattern = 'mobility' AND (
    LOWER(name) LIKE '%cars%' OR 
    LOWER(name) LIKE '%circles%'
);

-- Rollback smr pattern_subtype updates
UPDATE movements
SET pattern_subtype = CASE 
    WHEN LOWER(name) LIKE '%piriformis%' OR LOWER(name) LIKE '%hamstring%' OR 
         LOWER(name) LIKE '%lower back%' OR LOWER(name) LIKE '%iliotibial%' THEN 'hinge'::pattern_subtype
    WHEN LOWER(name) LIKE '%quadriceps%' THEN 'squat'::pattern_subtype
    WHEN LOWER(name) LIKE '%brachialis%' OR LOWER(name) LIKE '%latissimus%' OR 
         LOWER(name) LIKE '%rhomboids%' THEN 'horizontal_pull'::pattern_subtype
    WHEN LOWER(name) LIKE '%knee%' OR LOWER(name) LIKE '%neck%' OR 
         LOWER(name) LIKE '%calves%' OR LOWER(name) LIKE '%foot%' OR 
         LOWER(name) LIKE '%arm%' OR LOWER(name) LIKE '%hip%' THEN 'activation'::pattern_subtype
    WHEN LOWER(name) LIKE '%shoulder%' THEN 'vertical_push'::pattern_subtype
    ELSE 'carry'::pattern_subtype
END
WHERE pattern_subtype = 'smr';

-- Rollback conditioning pattern updates
UPDATE movements
SET pattern = NULL, pattern_subtype = NULL
WHERE pattern = 'conditioning' AND pattern_subtype = 'conditioning';

-- Rollback mobility pattern updates for discipline-based assignments
UPDATE movements
SET pattern = NULL, pattern_subtype = NULL
WHERE pattern = 'mobility' AND pattern_subtype = 'mobility'
  AND discipline IN ('mobility', 'stretch');

COMMIT;
