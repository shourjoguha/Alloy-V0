-- Migration: 20260301_add_rounds_and_circuit_flag
-- Add total_rounds and has_mini_circuit to hyrox_workouts_staging

-- ==== UP ====
ALTER TABLE hyrox_workouts_staging ADD COLUMN IF NOT EXISTS total_rounds INTEGER;
ALTER TABLE hyrox_workouts_staging ADD COLUMN IF NOT EXISTS has_mini_circuit BOOLEAN DEFAULT FALSE;

-- ==== DOWN ====
ALTER TABLE hyrox_workouts_staging DROP COLUMN IF EXISTS total_rounds;
ALTER TABLE hyrox_workouts_staging DROP COLUMN IF EXISTS has_mini_circuit;
