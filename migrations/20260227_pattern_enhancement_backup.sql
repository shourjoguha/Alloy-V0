-- BACKUP: Create backup of current movements table before pattern enhancement
-- This allows us to rollback if necessary

-- Create backup table
CREATE TABLE movements_backup_20260227 AS 
SELECT * FROM movements;

-- Verify backup was created
SELECT COUNT(*) as backup_count FROM movements_backup_20260227;
SELECT COUNT(*) as original_count FROM movements;

-- Show current pattern distribution
SELECT pattern, COUNT(*) as count 
FROM movements 
WHERE pattern IS NOT NULL 
GROUP BY pattern 
ORDER BY count DESC;

-- Show current discipline distribution  
SELECT discipline, COUNT(*) as count 
FROM movements 
WHERE discipline IS NOT NULL 
GROUP BY discipline 
ORDER BY count DESC;

-- Document current state
\echo 'BACKUP COMPLETED - movements_backup_20260227 table created'
\echo 'Original movements count: ' || (SELECT COUNT(*) FROM movements)
\echo 'Backup movements count: ' || (SELECT COUNT(*) FROM movements_backup_20260227)