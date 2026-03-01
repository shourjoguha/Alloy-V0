-- Migration: 20260301_add_hyrox_movements
-- Description: Add 6 new Hyrox movements to the database

-- ==== UP ====
BEGIN;

INSERT INTO movements (name, discipline, pattern, primary_region, primary_muscle, bodyweight_possible, dumbbell_possible, kettlebell_possible, barbell_possible, machine_possible, band_possible, plate_or_med_ball_possible)
VALUES
  ('Burpee Broad Jumps', 'crossfit', 'conditioning', 'full body', 'quadriceps', true, false, false, false, false, false, false),
  ('Calorie Ski Erg', 'cardio', 'conditioning', 'full body', 'full_body', false, false, false, false, true, false, false),
  ('V-Ups', 'resistance training', 'core', 'core', 'core', true, false, false, false, false, false, false),
  ('Sit-Ups', 'resistance training', 'core', 'core', 'core', true, false, false, false, false, false, false),
  ('Sandbag Lunges', 'resistance training', 'lunge', 'lower body', 'quadriceps', false, false, false, false, false, false, true),
  ('Lunges', 'resistance training', 'lunge', 'lower body', 'quadriceps', true, false, false, false, false, false, false)
RETURNING id, name;

COMMIT;

-- ==== DOWN ====
BEGIN;
DELETE FROM movements WHERE name IN ('Burpee Broad Jumps', 'Calorie Ski Erg', 'V-Ups', 'Sit-Ups', 'Sandbag Lunges', 'Lunges');
COMMIT;
