-- Migration: 20260227_enhance_pattern_column
-- Enhances the pattern column with granular pattern types for better movement selection
-- SAFE VERSION with backup and verification

-- ==== PRE-MIGRATION BACKUP ====
-- Create backup of current state (run this first separately if needed)
-- CREATE TABLE movements_backup_20260227 AS SELECT * FROM movements;

-- ==== UP ====
BEGIN;

-- Create a comprehensive pattern type enum
CREATE TYPE pattern_type AS ENUM (
    -- Core movement patterns
    'squat',
    'hinge', 
    'lunge',
    'horizontal_push',
    'horizontal_pull', 
    'vertical_push',
    'vertical_pull',
    'rotation',
    'carry',
    
    -- Athletic patterns
    'jump',
    'leap', 
    'hop',
    'bounding',
    'explosive',
    'sprint',
    'agility',
    
    -- Cardio patterns
    'run',
    'row',
    'bike',
    'cycle',
    'swim',
    'elliptical',
    'climb',
    
    -- Sled patterns
    'sled_push',
    'sled_pull',
    'sled_drag',
    
    -- Specialty patterns
    'burpee',
    'turkish_get_up',
    'farmer_carry',
    'waiter_carry',
    'suitcase_carry',
    'bear_crawl',
    'crab_walk',
    
    -- Mobility patterns
    'mobility',
    'stretch',
    'activation',
    'dynamic_warmup',
    'static_stretch',
    'foam_roll',
    
    -- Core stability
    'anti_extension',
    'anti_rotation', 
    'anti_lateral_flexion'
);

-- Add pattern_type column to movements table (NULLABLE initially for safety)
ALTER TABLE movements 
ADD COLUMN IF NOT EXISTS pattern_type pattern_type;

-- Create index for faster pattern-based queries
CREATE INDEX IF NOT EXISTS idx_movements_pattern_type ON movements(pattern_type);

-- Update existing patterns to new granular types based on current pattern values
-- This is a SAFE mapping that preserves existing functionality
UPDATE movements SET pattern_type = 'squat' WHERE pattern = 'squat' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'hinge' WHERE pattern = 'hinge' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'lunge' WHERE pattern = 'lunge' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'horizontal_push' WHERE pattern = 'horizontal_push' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'horizontal_pull' WHERE pattern = 'horizontal_pull' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'vertical_push' WHERE pattern = 'vertical_push' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'vertical_pull' WHERE pattern = 'vertical_pull' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'rotation' WHERE pattern = 'rotation' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'carry' WHERE pattern = 'carry' AND pattern_type IS NULL;

-- Map common movement names to appropriate patterns (only for unmapped movements)
UPDATE movements SET pattern_type = 'jump' WHERE name ILIKE '%jump%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'leap' WHERE name ILIKE '%leap%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'hop' WHERE name ILIKE '%hop%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'bounding' WHERE name ILIKE '%bound%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'explosive' WHERE name ILIKE '%explosive%' AND pattern_type IS NULL;

-- Map carries to specific carry patterns
UPDATE movements SET pattern_type = 'farmer_carry' WHERE name ILIKE '%farmer%' AND pattern_type = 'carry';
UPDATE movements SET pattern_type = 'waiter_carry' WHERE name ILIKE '%waiter%' AND pattern_type = 'carry';
UPDATE movements SET pattern_type = 'suitcase_carry' WHERE name ILIKE '%suitcase%' AND pattern_type = 'carry';

-- Map cardio patterns
UPDATE movements SET pattern_type = 'run' WHERE name ILIKE '%run%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'row' WHERE name ILIKE '%row%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'bike' WHERE name ILIKE '%bike%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'cycle' WHERE name ILIKE '%cycle%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'swim' WHERE name ILIKE '%swim%' AND pattern_type IS NULL;

-- Map sled patterns
UPDATE movements SET pattern_type = 'sled_push' WHERE name ILIKE '%sled%' AND name ILIKE '%push%';
UPDATE movements SET pattern_type = 'sled_pull' WHERE name ILIKE '%sled%' AND name ILIKE '%pull%';
UPDATE movements SET pattern_type = 'sled_drag' WHERE name ILIKE '%sled%' AND name ILIKE '%drag%';

-- Map specialty patterns
UPDATE movements SET pattern_type = 'burpee' WHERE name ILIKE '%burpee%';
UPDATE movements SET pattern_type = 'turkish_get_up' WHERE name ILIKE '%turkish%';
UPDATE movements SET pattern_type = 'bear_crawl' WHERE name ILIKE '%bear%' AND name ILIKE '%crawl%';
UPDATE movements SET pattern_type = 'crab_walk' WHERE name ILIKE '%crab%' AND name ILIKE '%walk%';

-- Map mobility patterns
UPDATE movements SET pattern_type = 'mobility' WHERE discipline IN ('mobility', 'stretch') AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'stretch' WHERE name ILIKE '%stretch%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'activation' WHERE name ILIKE '%activation%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'dynamic_warmup' WHERE name ILIKE '%dynamic%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'static_stretch' WHERE name ILIKE '%static%' AND pattern_type IS NULL;
UPDATE movements SET pattern_type = 'foam_roll' WHERE name ILIKE '%foam%' AND pattern_type IS NULL;

-- Set defaults for remaining movements based on discipline
UPDATE movements SET pattern_type = 'squat' WHERE discipline = 'resistance training' AND pattern_type IS NULL AND name ILIKE '%squat%';
UPDATE movements SET pattern_type = 'hinge' WHERE discipline = 'resistance training' AND pattern_type IS NULL AND name ILIKE '%deadlift%';
UPDATE movements SET pattern_type = 'horizontal_push' WHERE discipline = 'resistance training' AND pattern_type IS NULL AND name ILIKE '%bench%';
UPDATE movements SET pattern_type = 'horizontal_pull' WHERE discipline = 'resistance training' AND pattern_type IS NULL AND name ILIKE '%row%';
UPDATE movements SET pattern_type = 'vertical_push' WHERE discipline = 'resistance training' AND pattern_type IS NULL AND name ILIKE '%press%';
UPDATE movements SET pattern_type = 'vertical_pull' WHERE discipline = 'resistance training' AND pattern_type IS NULL AND name ILIKE '%pull%';

-- Final fallback for resistance training
UPDATE movements SET pattern_type = 'horizontal_push' WHERE discipline = 'resistance training' AND pattern_type IS NULL;

-- Verification: Show mapping results
SELECT 
    pattern_type, 
    COUNT(*) as count,
    STRING_AGG(DISTINCT pattern, ', ') as original_patterns
FROM movements 
WHERE pattern_type IS NOT NULL 
GROUP BY pattern_type 
ORDER BY count DESC;

-- Show movements that couldn't be mapped (should be minimal)
SELECT COUNT(*) as unmapped_movements 
FROM movements 
WHERE pattern_type IS NULL 
AND pattern IS NOT NULL;

COMMIT;
-- ==== DOWN ====
BEGIN;

-- Safe rollback - just remove the new column (preserves existing pattern column)
ALTER TABLE movements DROP COLUMN IF EXISTS pattern_type;
DROP TYPE IF EXISTS pattern_type;

COMMIT;