-- Pattern Subtype Mapping Verification Queries
-- Run these queries individually to verify the migration results

-- 1. Check total movements and mapping coverage
SELECT
    COUNT(*) as total_movements,
    COUNT(CASE WHEN pattern_subtype IS NOT NULL THEN 1 END) as mapped_movements,
    COUNT(CASE WHEN pattern_subtype IS NULL THEN 1 END) as unmapped_movements,
    ROUND(COUNT(CASE WHEN pattern_subtype IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as coverage_percentage
FROM movements;

-- 2. Pattern subtype distribution
SELECT
    pattern_subtype,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM movements), 2) as percentage,
    STRING_AGG(DISTINCT pattern::text, ', ' ORDER BY pattern::text) as original_patterns
FROM movements
WHERE pattern_subtype IS NOT NULL
GROUP BY pattern_subtype
ORDER BY count DESC;

-- 3. Show unmapped movements (first 20)
SELECT
    id,
    name,
    pattern::text as original_pattern,
    discipline::text as discipline
FROM movements
WHERE pattern_subtype IS NULL
ORDER BY name
LIMIT 20;

-- 4. Verify specific pattern mappings
SELECT
    pattern::text as original_pattern,
    pattern_subtype,
    COUNT(*) as count
FROM movements
WHERE pattern IN ('squat', 'hinge', 'lunge', 'horizontal_push', 'horizontal_pull', 'vertical_push', 'vertical_pull', 'rotation', 'carry')
GROUP BY pattern, pattern_subtype
ORDER BY pattern;

-- 5. Verify athletic pattern mappings (plyometric/isometric)
SELECT
    pattern_subtype,
    COUNT(*) as count,
    STRING_AGG(DISTINCT name, ', ') as examples
FROM movements
WHERE pattern_subtype IN ('plyometric', 'isometric')
GROUP BY pattern_subtype
ORDER BY pattern_subtype;

-- 6. Verify carry subtypes
SELECT
    pattern_subtype,
    COUNT(*) as count,
    STRING_AGG(DISTINCT name, ', ') as examples
FROM movements
WHERE pattern_subtype LIKE '%carry%'
GROUP BY pattern_subtype
ORDER BY pattern_subtype;

-- 7. Verify cardio patterns
SELECT
    pattern_subtype,
    COUNT(*) as count,
    STRING_AGG(DISTINCT name, ', ') as examples
FROM movements
WHERE pattern_subtype IN ('run', 'row', 'bike', 'cycle', 'swim')
GROUP BY pattern_subtype
ORDER BY pattern_subtype;

-- 8. Verify specialty patterns
SELECT
    pattern_subtype,
    COUNT(*) as count,
    STRING_AGG(DISTINCT name, ', ') as examples
FROM movements
WHERE pattern_subtype IN ('burpee', 'turkish_get_up', 'bear_crawl', 'crab_walk')
GROUP BY pattern_subtype
ORDER BY pattern_subtype;

-- 9. Verify mobility patterns
SELECT
    pattern_subtype,
    COUNT(*) as count,
    STRING_AGG(DISTINCT name, ', ') as examples
FROM movements
WHERE pattern_subtype IN ('mobility', 'stretch', 'activation', 'dynamic_warmup', 'static_stretch', 'foam_roll')
GROUP BY pattern_subtype
ORDER BY pattern_subtype;

-- 10. Example movements for each pattern subtype (up to 3 per subtype)
SELECT
    pattern_subtype,
    name,
    pattern::text as original_pattern,
    discipline::text as discipline
FROM (
    SELECT
        pattern_subtype,
        name,
        pattern,
        discipline,
        ROW_NUMBER() OVER (PARTITION BY pattern_subtype ORDER BY name) as rn
    FROM movements
    WHERE pattern_subtype IS NOT NULL
) ranked
WHERE rn <= 3
ORDER BY pattern_subtype, name;
