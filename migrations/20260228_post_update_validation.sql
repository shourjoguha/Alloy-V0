-- Migration: 20260228_post_update_validation
-- Purpose: Validate manual updates to movements table columns
-- Run this AFTER making manual changes to ensure data integrity

BEGIN;

-- 1. Check for NULL values in required columns
SELECT 
    'NULL CHECK' as validation_type,
    'primary_region should never be NULL' as check_description,
    COUNT(*) as failed_count
FROM movements 
WHERE primary_region IS NULL;

-- 2. Validate boolean columns (should be true, false, or NULL - never other values)
SELECT 
    'BOOLEAN VALIDATION' as validation_type,
    'Invalid boolean values in equipment columns' as check_description,
    COUNT(*) as failed_count
FROM movements 
WHERE 
    bodyweight_possible NOT IN (true, false, NULL) OR
    dumbbell_possible NOT IN (true, false, NULL) OR
    kettlebell_possible NOT IN (true, false, NULL) OR
    barbell_possible NOT IN (true, false, NULL) OR
    machine_possible NOT IN (true, false, NULL) OR
    band_possible NOT IN (true, false, NULL) OR
    plate_or_med_ball_possible NOT IN (true, false, NULL);

-- 3. Validate primary_region enum values
DO $$
DECLARE
    invalid_regions INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_regions
    FROM movements m
    WHERE m.primary_region NOT IN (
        SELECT enumlabel::primaryregion 
        FROM pg_enum 
        WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'primaryregion')
    );
    
    IF invalid_regions > 0 THEN
        RAISE NOTICE 'WARNING: Found % movements with invalid primary_region values', invalid_regions;
        RAISE NOTICE 'Run this query to see invalid values: SELECT id, name, primary_region FROM movements WHERE primary_region NOT IN (SELECT enumlabel::primaryregion FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = ''primaryregion'')) LIMIT 10;';
    ELSE
        RAISE NOTICE 'PASS: All primary_region values are valid enum values';
    END IF;
END $$;

-- 4. Validate pattern enum values
DO $$
DECLARE
    invalid_patterns INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_patterns
    FROM movements m
    WHERE m.pattern NOT IN (
        SELECT enumlabel::patterntype_new 
        FROM pg_enum 
        WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'patterntype_new')
    ) AND m.pattern IS NOT NULL;
    
    IF invalid_patterns > 0 THEN
        RAISE NOTICE 'WARNING: Found % movements with invalid pattern values', invalid_patterns;
        RAISE NOTICE 'Run this query to see invalid values: SELECT id, name, pattern FROM movements WHERE pattern NOT IN (SELECT enumlabel::patterntype_new FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = ''patterntype_new'')) AND pattern IS NOT NULL LIMIT 10;';
    ELSE
        RAISE NOTICE 'PASS: All pattern values are valid enum values';
    END IF;
END $$;

-- 5. Validate pattern_subtype enum values
DO $$
DECLARE
    invalid_subtypes INTEGER;
BEGIN
    SELECT COUNT(*) INTO invalid_subtypes
    FROM movements m
    WHERE m.pattern_subtype NOT IN (
        SELECT enumlabel::pattern_subtype 
        FROM pg_enum 
        WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = 'pattern_subtype')
    ) AND m.pattern_subtype IS NOT NULL;
    
    IF invalid_subtypes > 0 THEN
        RAISE NOTICE 'WARNING: Found % movements with invalid pattern_subtype values', invalid_subtypes;
        RAISE NOTICE 'Run this query to see invalid values: SELECT id, name, pattern_subtype FROM movements WHERE pattern_subtype NOT IN (SELECT enumlabel::pattern_subtype FROM pg_enum WHERE enumtypid = (SELECT oid FROM pg_type WHERE typname = ''pattern_subtype'')) AND pattern_subtype IS NOT NULL LIMIT 10;';
    ELSE
        RAISE NOTICE 'PASS: All pattern_subtype values are valid enum values';
    END IF;
END $$;

-- 6. Summary statistics for comparison
SELECT 
    'SUMMARY STATS' as section,
    'Total movements' as metric,
    COUNT(*) as value
FROM movements
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Non-null primary_region' as metric,
    COUNT(*)
FROM movements 
WHERE primary_region IS NOT NULL
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Non-null pattern' as metric,
    COUNT(*)
FROM movements 
WHERE pattern IS NOT NULL
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Non-null pattern_subtype' as metric,
    COUNT(*)
FROM movements 
WHERE pattern_subtype IS NOT NULL
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Bodyweight possible' as metric,
    COUNT(*)
FROM movements 
WHERE bodyweight_possible = true
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Dumbbell possible' as metric,
    COUNT(*)
FROM movements 
WHERE dumbbell_possible = true
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Barbell possible' as metric,
    COUNT(*)
FROM movements 
WHERE barbell_possible = true
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Kettlebell possible' as metric,
    COUNT(*)
FROM movements 
WHERE kettlebell_possible = true
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Machine possible' as metric,
    COUNT(*)
FROM movements 
WHERE machine_possible = true
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Band possible' as metric,
    COUNT(*)
FROM movements 
WHERE band_possible = true
UNION ALL
SELECT 
    'SUMMARY STATS' as section,
    'Plate/Med ball possible' as metric,
    COUNT(*)
FROM movements 
WHERE plate_or_med_ball_possible = true;

COMMIT;

-- Additional manual validation queries (run as needed):
-- 
-- 1. See all distinct values for a column:
-- SELECT DISTINCT primary_region, COUNT(*) FROM movements GROUP BY primary_region ORDER BY primary_region;
--
-- 2. Find movements with no equipment set:
-- SELECT id, name FROM movements WHERE 
--     bodyweight_possible = false AND
--     dumbbell_possible = false AND
--     kettlebell_possible = false AND
--     barbell_possible = false AND
--     machine_possible = false AND
--     band_possible = false AND
--     plate_or_med_ball_possible = false;
--
-- 3. Compare with backup:
-- SELECT m.id, m.name, m.primary_region as new_region, b.primary_region as old_region 
-- FROM movements m 
-- LEFT JOIN movements_backup_20260228 b ON m.id = b.id 
-- WHERE m.primary_region IS DISTINCT FROM b.primary_region;
