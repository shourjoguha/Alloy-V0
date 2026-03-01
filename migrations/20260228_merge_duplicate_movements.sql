-- Migration: 20260228_merge_duplicate_movements
-- Purpose: Merge duplicate movements and update all references
-- 

-- ==== UP ====
BEGIN;

-- Set transaction isolation level to prevent concurrent modification issues
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Create temporary table to track merges
CREATE TEMP TABLE movement_merges (
  canonical_id INTEGER,
  duplicate_id INTEGER,
  original_name TEXT
);

-- Insert merge mappings based on circuit usage priority
INSERT INTO movement_merges (canonical_id, duplicate_id, original_name) VALUES
-- Set 1: 491 and 3 -> Keep 491 (has 3 circuit references)
(491, 3, 'Goblet Squat'),

-- Set 2: 131, 576, 617 -> Keep 131 (has 2 circuit references, first in list)
(131, 576, 'Crunch Legs On Exercise Ball'),
(131, 617, 'Sit Up'),

-- Set 3: 389 and 264 -> Keep 389 (has 7 circuit references)
(389, 264, 'Running, Treadmill'),

-- Set 4: SMR variations - keep first (all have 0 circuit references)
(245, 688, 'Quadriceps Smr'),
(231, 686, 'Piriformis Smr'),
(369, 710, 'Upper Back Leg Grab'),
(75, 661, 'Anterior Tibialis Smr'),
(116, 665, 'Calves Smr'),
(98, 663, 'Brachialis Smr'),
(194, 677, 'Latissimus Dorsi Smr'),

-- Set 5: Push-up variations -> Keep 16 (has 2 circuit references)
(16, 607, 'Push Ups With Feet Elevated'),
(16, 239, 'Push-Ups With Feet Elevated'),
(16, 588, 'Incline Push Up'),
(16, 591, 'Incline Push Up Reverse Grip'),
(16, 606, 'Push Ups Close Triceps Position'),
(16, 238, 'Push-Ups-Close Triceps Position'),

-- Set 6: 635 and 636 -> Keep 635 (first in list, both 0 circuit references)
(635, 636, 'Hang Snatch Below Knees'),

-- Set 7: 524 and 115 -> Keep 524 (first in list, both 0 circuit references)
(524, 115, 'Calf Stretch Hands Against Wall'),

-- Set 8: 512 and 213 -> Keep 512 (first in list, both 0 circuit references)
(512, 213, 'Mountain Climbers'),

-- Set 9: 536, 254, 253 -> Keep 536 (first in list, all 0 circuit references)
(536, 254, 'Reverse Flyes'),
(536, 253, 'Reverse Flyes With External Rotation'),

-- Set 10: 383 and 262 -> Keep 383 (has 7 circuit references)
(383, 262, 'Rope Jumping'),

-- Set 11: 8 and 651 -> Keep 8 (first in list, both 0 circuit references)
(8, 651, 'Romanian Deadlift From Deficit'),

-- Set 12: 613 and 357 -> Keep 613 (first in list, both 0 circuit references)
(613, 357, 'Seated Flat Bench Leg Pull-In'),

-- Set 13: 692 and 271 -> Keep 692 (first in list, both 0 circuit references)
(692, 271, 'Seated Hamstring'),

-- Set 14: 614 and 537 -> Keep 614 (first in list, both 0 circuit references)
(614, 537, 'Seated Leg Raise'),

-- Set 15: 21 and 501 -> Keep 501 (has 1 circuit reference)
(501, 21, 'Handstand Push-Up'),

-- Set 16: 260 and 502 -> Keep 502 (has 1 circuit reference)
(502, 260, 'Ring Dips'),

-- Set 17: 708 and 709 -> Keep 708 (first in list, both 0 circuit references)
(708, 709, 'Triceps Stretch');

-- Display what will be merged
SELECT 'Movement Merges:' as operation;
SELECT 
  mm.canonical_id,
  (SELECT name FROM movements WHERE id = mm.canonical_id) as canonical_name,
  mm.duplicate_id,
  mm.original_name as duplicate_name,
  (SELECT COUNT(*) FROM circuits_melted WHERE movement_id = mm.duplicate_id) as affected_circuits
FROM movement_merges mm
ORDER BY mm.canonical_id, mm.duplicate_id;

-- Update all table references to point to canonical movements

-- 1. Update circuits_melted
SELECT 'Updating circuits_melted references...' as operation;
UPDATE circuits_melted
SET movement_id = mm.canonical_id
FROM movement_merges mm
WHERE circuits_melted.movement_id = mm.duplicate_id;

-- 2. Update movement_coaching_cues
SELECT 'Updating movement_coaching_cues references...' as operation;
UPDATE movement_coaching_cues
SET movement_id = mm.canonical_id
FROM movement_merges mm
WHERE movement_coaching_cues.movement_id = mm.duplicate_id;

-- 3. Update movement_equipment
SELECT 'Updating movement_equipment references...' as operation;
UPDATE movement_equipment
SET movement_id = mm.canonical_id
FROM movement_merges mm
WHERE movement_equipment.movement_id = mm.duplicate_id;

-- 4. Update movement_muscle_map
SELECT 'Updating movement_muscle_map references...' as operation;
UPDATE movement_muscle_map
SET movement_id = mm.canonical_id
FROM movement_merges mm
WHERE movement_muscle_map.movement_id = mm.duplicate_id;

-- Display summary of updated records
SELECT 'Summary of updates:' as operation;
SELECT 
  'circuits_melted' as table_name,
  COUNT(*) as records_updated
FROM circuits_melted cm
JOIN movement_merges mm ON cm.movement_id = mm.canonical_id
UNION ALL
SELECT 
  'movement_coaching_cues' as table_name,
  COUNT(*) as records_updated
FROM movement_coaching_cues mc
JOIN movement_merges mm ON mc.movement_id = mm.canonical_id
UNION ALL
SELECT 
  'movement_equipment' as table_name,
  COUNT(*) as records_updated
FROM movement_equipment me
JOIN movement_merges mm ON me.movement_id = mm.canonical_id
UNION ALL
SELECT 
  'movement_muscle_map' as table_name,
  COUNT(*) as records_updated
FROM movement_muscle_map mm2
JOIN movement_merges mm ON mm2.movement_id = mm.canonical_id
ORDER BY table_name;

-- Delete duplicate movements
DELETE FROM movements
WHERE id IN (SELECT duplicate_id FROM movement_merges);

-- Display deletion summary
SELECT 'Deleted duplicate movements:' as operation;
SELECT 
  mm.duplicate_id,
  mm.original_name
FROM movement_merges mm
ORDER BY mm.duplicate_id;

-- Verify no orphaned references remain
SELECT 'Verification - Checking for orphaned references:' as operation;

-- Check circuits_melted
SELECT 
  'circuits_melted' as table_name,
  COUNT(*) as orphaned_count
FROM circuits_melted cm
WHERE cm.movement_id IS NOT NULL 
  AND NOT EXISTS (SELECT 1 FROM movements WHERE id = cm.movement_id)
UNION ALL
-- Check movement_coaching_cues
SELECT 
  'movement_coaching_cues' as table_name,
  COUNT(*) as orphaned_count
FROM movement_coaching_cues mc
WHERE mc.movement_id IS NOT NULL 
  AND NOT EXISTS (SELECT 1 FROM movements WHERE id = mc.movement_id)
UNION ALL
-- Check movement_equipment
SELECT 
  'movement_equipment' as table_name,
  COUNT(*) as orphaned_count
FROM movement_equipment me
WHERE me.movement_id IS NOT NULL 
  AND NOT EXISTS (SELECT 1 FROM movements WHERE id = me.movement_id)
UNION ALL
-- Check movement_muscle_map
SELECT 
  'movement_muscle_map' as table_name,
  COUNT(*) as orphaned_count
FROM movement_muscle_map mm2
WHERE mm2.movement_id IS NOT NULL 
  AND NOT EXISTS (SELECT 1 FROM movements WHERE id = mm2.movement_id);

-- Should return 0 for all tables if successful

-- Drop temporary table
DROP TABLE movement_merges;

COMMIT;

-- Display final statistics
SELECT 
  'Migration Complete' as status,
  COUNT(*) as remaining_movements
FROM movements;

-- ==== DOWN ====
BEGIN;

-- Note: This rollback is limited - it cannot restore deleted movements
-- For full rollback, you would need to restore from backup
-- This script only updates references back to their original state
-- (which would still result in orphaned references)

-- Warning: Cannot fully rollback movement deletions
RAISE NOTICE 'WARNING: This rollback cannot restore deleted movements. Restore from backup if needed.';

ROLLBACK;
