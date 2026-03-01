#!/bin/bash
# Pattern Subtype Mapping Verification - Simple Shell Script
# This script uses non-interactive docker exec to avoid hanging issues

CONTAINER="43664739cb71cd5f334347f8b4d5e1de4f7a1379c2449294687de3ab2f9f1454"
DB_NAME="Jacked-DB"
DB_USER="jacked"

echo "======================================"
echo "Pattern Subtype Verification Report"
echo "======================================"
echo ""

# 1. Total movements and coverage
echo "1. Coverage Statistics:"
echo "----------------------"
docker exec "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "
SELECT
    COUNT(*) as total_movements,
    COUNT(CASE WHEN pattern_subtype IS NOT NULL THEN 1 END) as mapped_movements,
    COUNT(CASE WHEN pattern_subtype IS NULL THEN 1 END) as unmapped_movements,
    ROUND(COUNT(CASE WHEN pattern_subtype IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 2) as coverage_percentage
FROM movements;
"
echo ""

# 2. Pattern subtype distribution
echo "2. Pattern Subtype Distribution:"
echo "---------------------------------"
docker exec "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "
SELECT
    pattern_subtype,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM movements), 2) as percentage
FROM movements
WHERE pattern_subtype IS NOT NULL
GROUP BY pattern_subtype
ORDER BY count DESC;
"
echo ""

# 3. Unmapped movements
echo "3. Unmapped Movements (first 10):"
echo "---------------------------------"
docker exec "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "
SELECT
    name,
    pattern::text as original_pattern,
    discipline::text as discipline
FROM movements
WHERE pattern_subtype IS NULL
ORDER BY name
LIMIT 10;
"
echo ""

# 4. Core pattern mappings
echo "4. Core Pattern Mappings:"
echo "-------------------------"
docker exec "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "
SELECT
    pattern::text as original_pattern,
    pattern_subtype,
    COUNT(*) as count
FROM movements
WHERE pattern IN ('squat', 'hinge', 'lunge', 'horizontal_push', 'horizontal_pull', 'vertical_push', 'vertical_pull', 'rotation', 'carry')
GROUP BY pattern, pattern_subtype
ORDER BY pattern;
"
echo ""

# 5. Athletic patterns
echo "5. Athletic Pattern Mappings:"
echo "-----------------------------"
docker exec "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "
SELECT
    pattern_subtype,
    COUNT(*) as count
FROM movements
WHERE pattern_subtype IN ('plyometric', 'isometric')
GROUP BY pattern_subtype;
"
echo ""

echo "======================================"
echo "Verification Complete"
echo "======================================"
