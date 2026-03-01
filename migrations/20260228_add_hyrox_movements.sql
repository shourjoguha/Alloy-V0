-- Migration: 20260228_add_hyrox_movements
-- Description: Add 6 new Hyrox-specific movements to the movements table
-- ==== UP ====
BEGIN;

-- Insert new Hyrox movements
INSERT INTO movements (name, discipline, pattern, primary_region, primary_muscle, bodyweight_possible, dumbbell_possible, kettlebell_possible, barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible) VALUES
('Burpee Broad Jumps', 'crossfit', 'conditioning', 'full body', 'quadriceps', true, false, false, false, false, false, false),
('Calorie Ski Erg', 'cardio', 'conditioning', 'full body', 'full_body', false, false, false, false, true, false, false),
('V-Ups', 'resistance training', 'core', 'core', 'core', true, false, false, false, false, false, false),
('Sit-Ups', 'resistance training', 'core', 'core', 'core', true, false, false, false, false, false, false),
('Sandbag Lunges', 'resistance training', 'lunge', 'lower body', 'quadriceps', false, false, false, false, false, false, true),
('Lunges', 'resistance training', 'lunge', 'lower body', 'quadriceps', true, false, false, false, false, false, false);

-- Get the IDs of the newly inserted movements
DO $$
DECLARE
  burpee_broad_jumps_id INTEGER;
  calorie_ski_erg_id INTEGER;
  v_ups_id INTEGER;
  sit_ups_id INTEGER;
  sandbag_lunges_id INTEGER;
  lunges_id INTEGER;
BEGIN
  SELECT id INTO burpee_broad_jumps_id FROM movements WHERE name = 'Burpee Broad Jumps';
  SELECT id INTO calorie_ski_erg_id FROM movements WHERE name = 'Calorie Ski Erg';
  SELECT id INTO v_ups_id FROM movements WHERE name = 'V-Ups';
  SELECT id INTO sit_ups_id FROM movements WHERE name = 'Sit-Ups';
  SELECT id INTO sandbag_lunges_id FROM movements WHERE name = 'Sandbag Lunges';
  SELECT id INTO lunges_id FROM movements WHERE name = 'Lunges';
  
  RAISE NOTICE 'New movement IDs: Burpee Broad Jumps=%, Calorie Ski Erg=%, V-Ups=%, Sit-Ups=%, Sandbag Lunges=%, Lunges=%', 
    burpee_broad_jumps_id, calorie_ski_erg_id, v_ups_id, sit_ups_id, sandbag_lunges_id, lunges_id;
END $$;

COMMIT;
-- ==== DOWN ====
BEGIN;
-- Remove the new movements if rollback is needed
DELETE FROM movements WHERE name IN (
  'Burpee Broad Jumps',
  'Calorie Ski Erg',
  'V-Ups',
  'Sit-Ups',
  'Sandbag Lunges',
  'Lunges'
);
COMMIT;
