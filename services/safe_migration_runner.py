"""
Safe Database Migration Runner for Alloy AI Fitness System
Executes migrations with comprehensive error logging and rollback capabilities.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from services.error_logger import log_migration_error, error_logger


class SafeMigrationRunner:
    """Safe migration execution with error logging and rollback capabilities."""
    
    def __init__(self, db_session: AsyncSession):
        """Initialize with database session."""
        self.db = db_session
        self.migration_log = []
        self.current_migration = None
    
    async def execute_migration(
        self,
        migration_sql: str,
        migration_name: str,
        backup_before: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a migration with comprehensive error handling and logging.
        
        Args:
            migration_sql: SQL migration script
            migration_name: Name of the migration for logging
            backup_before: Whether to create backup before migration
            dry_run: Whether to simulate the migration without executing
            
        Returns:
            Result dictionary with success status and details
        """
        self.current_migration = migration_name
        start_time = datetime.utcnow()
        
        result = {
            "migration_name": migration_name,
            "success": False,
            "start_time": start_time.isoformat(),
            "end_time": None,
            "affected_rows": 0,
            "backup_created": False,
            "errors": [],
            "warnings": [],
            "details": {}
        }
        
        try:
            # Create backup if requested
            if backup_before and not dry_run:
                backup_result = await self._create_backup(migration_name)
                result["backup_created"] = backup_result["success"]
                if not backup_result["success"]:
                    result["errors"].extend(backup_result["errors"])
                    return result
            
            # Parse migration SQL to separate UP and DOWN sections
            migration_parts = self._parse_migration_sql(migration_sql)
            
            if dry_run:
                # Simulate migration execution
                dry_run_result = await self._simulate_migration(migration_parts)
                result.update(dry_run_result)
                result["success"] = len(result["errors"]) == 0
                return result
            
            # Execute UP migration
            up_result = await self._execute_migration_part(
                migration_parts["up"],
                migration_name,
                "UP"
            )
            
            result.update(up_result)
            result["success"] = len(result["errors"]) == 0
            
            # Log migration completion
            end_time = datetime.utcnow()
            result["end_time"] = end_time.isoformat()
            result["duration_seconds"] = (end_time - start_time).total_seconds()
            
            if result["success"]:
                self._log_migration_success(migration_name, result)
            else:
                # Attempt rollback if migration failed
                rollback_result = await self._attempt_rollback(migration_parts["down"], migration_name)
                result["rollback_attempted"] = True
                result["rollback_success"] = rollback_result["success"]
                if not rollback_result["success"]:
                    result["errors"].extend(rollback_result["errors"])
            
            return result
            
        except Exception as e:
            # Log unexpected error
            trace_id = log_migration_error(
                migration_name=migration_name,
                error=e,
                sql_query=migration_sql[:500],  # Truncate for logging
                context={"migration_step": "execution", "dry_run": dry_run}
            )
            
            result["errors"].append(f"Unexpected error during migration: {str(e)}")
            result["trace_id"] = trace_id
            result["end_time"] = datetime.utcnow().isoformat()
            
            return result
    
    async def _create_backup(self, migration_name: str) -> Dict[str, Any]:
        """Create backup of movements table before migration."""
        backup_result = {
            "success": False,
            "backup_table": f"movements_backup_{migration_name.lower().replace(' ', '_')}",
            "errors": [],
            "warnings": []
        }
        
        try:
            # Check if backup table already exists
            check_query = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = :table_name
                )
            """)
            
            result = await self.db.execute(check_query, {"table_name": backup_result["backup_table"]})
            table_exists = result.scalar()
            
            if table_exists:
                backup_result["warnings"].append(f"Backup table {backup_result['backup_table']} already exists")
                backup_result["success"] = True
                return backup_result
            
            # Create backup table
            backup_sql = f"""
                CREATE TABLE {backup_result['backup_table']} AS 
                SELECT * FROM movements;
            """
            
            await self.db.execute(text(backup_sql))
            
            # Verify backup
            count_query = text(f"SELECT COUNT(*) FROM {backup_result['backup_table']}")
            result = await self.db.execute(count_query)
            backup_count = result.scalar()
            
            original_count_query = text("SELECT COUNT(*) FROM movements")
            result = await self.db.execute(original_count_query)
            original_count = result.scalar()
            
            if backup_count != original_count:
                backup_result["warnings"].append(
                    f"Backup count mismatch: backed up {backup_count} rows, original has {original_count} rows"
                )
            
            backup_result["backup_row_count"] = backup_count
            backup_result["original_row_count"] = original_count
            backup_result["success"] = True
            
        except Exception as e:
            error_msg = f"Failed to create backup: {str(e)}"
            backup_result["errors"].append(error_msg)
            log_migration_error(
                migration_name=migration_name,
                error=e,
                context={"migration_step": "backup_creation"}
            )
        
        return backup_result
    
    def _parse_migration_sql(self, migration_sql: str) -> Dict[str, str]:
        """Parse migration SQL to separate UP and DOWN sections."""
        parts = {"up": "", "down": ""}
        current_part = "up"
        
        for line in migration_sql.split('\n'):
            line_stripped = line.strip()
            
            if line_stripped.upper() == "-- ==== DOWN ====":
                current_part = "down"
                continue
            elif line_stripped.upper() == "-- ==== UP ====":
                current_part = "up"
                continue
            
            parts[current_part] += line + '\n'
        
        return parts
    
    async def _simulate_migration(self, migration_parts: Dict[str, str]) -> Dict[str, Any]:
        """Simulate migration execution without actually running it."""
        simulation_result = {
            "simulated": True,
            "up_sql_lines": len(migration_parts["up"].strip().split('\n')),
            "down_sql_lines": len(migration_parts["down"].strip().split('\n')),
            "warnings": [],
            "errors": []
        }
        
        try:
            # Analyze UP section
            up_sql = migration_parts["up"].strip()
            if not up_sql:
                simulation_result["errors"].append("UP section is empty")
            
            # Check for common migration patterns
            if "CREATE TYPE" in up_sql:
                simulation_result["warnings"].append("Creating new ENUM type - ensure compatibility")
            
            if "ALTER TABLE" in up_sql and "ADD COLUMN" in up_sql:
                simulation_result["warnings"].append("Adding new column - ensure proper indexing")
            
            if "CREATE INDEX" in up_sql:
                simulation_result["warnings"].append("Creating indexes - may take time on large tables")
            
            # Analyze DOWN section
            down_sql = migration_parts["down"].strip()
            if not down_sql:
                simulation_result["warnings"].append("DOWN section is empty - rollback not possible")
            
            # Check for DROP statements
            if "DROP COLUMN" in down_sql:
                simulation_result["warnings"].append("DOWN section drops columns - data loss on rollback")
            
            if "DROP TYPE" in down_sql:
                simulation_result["warnings"].append("DOWN section drops types - ensure no dependencies")
            
        except Exception as e:
            simulation_result["errors"].append(f"Simulation failed: {str(e)}")
        
        return simulation_result
    
    async def _execute_migration_part(
        self,
        sql_part: str,
        migration_name: str,
        part_name: str
    ) -> Dict[str, Any]:
        """Execute a specific part of the migration (UP or DOWN)."""
        result = {
            "success": False,
            "affected_rows": 0,
            "errors": [],
            "warnings": [],
            "statements_executed": 0
        }
        
        if not sql_part.strip():
            result["warnings"].append(f"{part_name} section is empty")
            result["success"] = True
            return result
        
        try:
            # Split SQL into individual statements
            statements = self._split_sql_statements(sql_part)
            
            for i, statement in enumerate(statements):
                if not statement.strip():
                    continue
                
                # Execute statement
                exec_result = await self.db.execute(text(statement))
                
                # Get affected rows if possible
                try:
                    affected_rows = exec_result.rowcount if hasattr(exec_result, 'rowcount') else 0
                    result["affected_rows"] += affected_rows
                except:
                    pass  # Not all statements return rowcount
                
                result["statements_executed"] += 1
                
                # Log successful statement execution
                self._log_statement_success(migration_name, part_name, i + 1, statement[:100])
            
            result["success"] = True
            
        except Exception as e:
            error_msg = f"Failed to execute {part_name} section: {str(e)}"
            result["errors"].append(error_msg)
            
            # Log the error with full context
            log_migration_error(
                migration_name=migration_name,
                error=e,
                sql_query=sql_part[:500],
                context={"migration_part": part_name, "statements_executed": result["statements_executed"]}
            )
        
        return result
    
    def _split_sql_statements(self, sql: str) -> List[str]:
        """Split SQL into individual statements."""
        statements = []
        current_statement = ""
        
        for line in sql.split('\n'):
            line_stripped = line.strip()
            
            # Skip empty lines and comments
            if not line_stripped or line_stripped.startswith('--'):
                continue
            
            current_statement += line + '\n'
            
            # Check if statement is complete (ends with semicolon)
            if line_stripped.endswith(';'):
                statements.append(current_statement.strip())
                current_statement = ""
        
        # Add remaining statement if any
        if current_statement.strip():
            statements.append(current_statement.strip())
        
        return statements
    
    async def _attempt_rollback(self, down_sql: str, migration_name: str) -> Dict[str, Any]:
        """Attempt to rollback a failed migration."""
        rollback_result = {
            "success": False,
            "errors": [],
            "warnings": []
        }
        
        try:
            if not down_sql.strip():
                rollback_result["warnings"].append("No DOWN section available for rollback")
                return rollback_result
            
            # Execute DOWN migration
            rollback_exec = await self._execute_migration_part(
                down_sql,
                migration_name,
                "ROLLBACK"
            )
            
            rollback_result.update(rollback_exec)
            
            if rollback_exec["success"]:
                self._log_rollback_success(migration_name, rollback_exec)
            else:
                rollback_result["errors"].extend(rollback_exec["errors"])
            
        except Exception as e:
            error_msg = f"Rollback attempt failed: {str(e)}"
            rollback_result["errors"].append(error_msg)
            log_migration_error(
                migration_name=migration_name,
                error=e,
                context={"migration_step": "rollback_attempt"}
            )
        
        return rollback_result
    
    def _log_migration_success(self, migration_name: str, result: Dict[str, Any]) -> None:
        """Log successful migration completion."""
        success_log = {
            "event": "migration_success",
            "migration_name": migration_name,
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": result.get("duration_seconds", 0),
            "affected_rows": result.get("affected_rows", 0),
            "statements_executed": result.get("statements_executed", 0)
        }
        
        print(f"✅ Migration '{migration_name}' completed successfully")
        print(f"   Duration: {result.get('duration_seconds', 0):.2f}s")
        print(f"   Affected rows: {result.get('affected_rows', 0)}")
        print(f"   Statements executed: {result.get('statements_executed', 0)}")
    
    def _log_statement_success(self, migration_name: str, part_name: str, statement_num: int, statement_preview: str) -> None:
        """Log successful statement execution."""
        # This could be enhanced with more detailed logging
        pass
    
    def _log_rollback_success(self, migration_name: str, rollback_result: Dict[str, Any]) -> None:
        """Log successful rollback."""
        print(f"⚠️  Migration '{migration_name}' rolled back successfully")
        print(f"   Rollback statements executed: {rollback_result.get('statements_executed', 0)}")


# Convenience function for running migrations
async def run_migration_safely(
    db_session: AsyncSession,
    migration_sql: str,
    migration_name: str,
    backup_before: bool = True,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to run a migration safely with error logging.
    
    Args:
        db_session: Database session
        migration_sql: SQL migration script
        migration_name: Name of the migration
        backup_before: Whether to create backup before migration
        dry_run: Whether to simulate the migration
        
    Returns:
        Migration result dictionary
    """
    runner = SafeMigrationRunner(db_session)
    return await runner.execute_migration(
        migration_sql=migration_sql,
        migration_name=migration_name,
        backup_before=backup_before,
        dry_run=dry_run
    )