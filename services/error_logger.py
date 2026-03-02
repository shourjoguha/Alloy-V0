"""
Enhanced Error Logging System for Alloy AI Fitness System
Provides comprehensive error tracking and debugging for database migrations and program generation.
"""

import logging
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import uuid


class EnhancedErrorLogger:
    """Comprehensive error logging system with structured output and external service integration."""
    
    def __init__(self, log_file_path: Optional[Path] = None, environment: str = "development"):
        """Initialize error logger with file path and environment."""
        if log_file_path is None:
            log_file_path = Path(__file__).parent.parent / "logs" / "error_logs.jsonl"
        
        self.log_file_path = log_file_path
        self.environment = environment
        
        # Ensure log directory exists before setting up logger
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup structured logger with JSON formatting."""
        logger = logging.getLogger("alloy_ai_error_logger")
        logger.setLevel(logging.ERROR)
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler with JSON formatting
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.ERROR)
        
        # Custom JSON formatter
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        return logger
    
    def log_error(
        self,
        error_code: str,
        error_message: str,
        error_details: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> str:
        """
        Log error with standardized format following project rules.
        
        Args:
            error_code: Standardized error code (e.g., "DB_MIGRATION_FAILED")
            error_message: Human-readable error message
            error_details: Technical details about the error
            context: Additional context (user_id, request_data, etc.)
            trace_id: Unique trace identifier for tracking
            
        Returns:
            trace_id for error correlation
        """
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        error_entry = {
            "error": {
                "code": error_code,
                "message": error_message,
                "details": error_details,
                "trace_id": trace_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "environment": self.environment
            },
            "context": context or {}
        }
        
        # Log to file as JSON
        self.logger.error(json.dumps(error_entry))
        
        # Also log to external service in production
        if self.environment == "production":
            self._log_to_external_service(error_entry)
        
        return trace_id
    
    def log_migration_error(
        self,
        migration_name: str,
        error: Exception,
        sql_query: Optional[str] = None,
        affected_rows: int = 0,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Specialized error logging for database migrations.
        
        Args:
            migration_name: Name of the migration that failed
            error: The exception that occurred
            sql_query: SQL query that caused the error
            affected_rows: Number of rows affected before failure
            context: Additional migration context
            
        Returns:
            trace_id for error correlation
        """
        error_details = {
            "migration_name": migration_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "sql_query": sql_query,
            "affected_rows": affected_rows,
            "stack_trace": traceback.format_exc()
        }
        
        return self.log_error(
            error_code="DB_MIGRATION_FAILED",
            error_message=f"Database migration '{migration_name}' failed",
            error_details=error_details,
            context=context
        )
    
    def log_program_generation_error(
        self,
        error: Exception,
        request_data: Optional[Dict[str, Any]] = None,
        validation_errors: Optional[list] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Specialized error logging for program generation failures.
        
        Args:
            error: The exception that occurred
            request_data: Original request data
            validation_errors: List of validation errors
            context: Additional context
            
        Returns:
            trace_id for error correlation
        """
        error_details = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "validation_errors": validation_errors or [],
            "stack_trace": traceback.format_exc()
        }
        
        context_data = context or {}
        if request_data:
            context_data["request_data"] = request_data
        
        return self.log_error(
            error_code="PROGRAM_GENERATION_FAILED",
            error_message="Program generation failed",
            error_details=error_details,
            context=context_data
        )
    
    def log_validation_error(
        self,
        validation_errors: list,
        request_data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Specialized error logging for validation failures.
        
        Args:
            validation_errors: List of validation error messages
            request_data: Original request data
            context: Additional context
            
        Returns:
            trace_id for error correlation
        """
        error_details = {
            "validation_errors": validation_errors,
            "error_count": len(validation_errors)
        }
        
        context_data = context or {}
        if request_data:
            context_data["request_data"] = request_data
        
        return self.log_error(
            error_code="VALIDATION_FAILED",
            error_message="Input validation failed",
            error_details=error_details,
            context=context_data
        )
    
    def _log_to_external_service(self, error_entry: Dict[str, Any]) -> None:
        """
        Log to external service (Sentry, Datadog, etc.) in production.
        This is a placeholder - implement actual external service integration.
        """
        try:
            # Placeholder for external service integration
            # In production, this would send to Sentry, Datadog, etc.
            # For now, we'll just log that we're attempting external logging
            self.logger.error(f"Attempting external service logging for trace_id: {error_entry['error']['trace_id']}")
        except Exception as e:
            # Don't let external logging failures mask the original error
            self.logger.error(f"Failed to log to external service: {str(e)}")
    
    def get_recent_errors(self, limit: int = 10) -> list:
        """
        Retrieve recent errors from log file for debugging.
        
        Args:
            limit: Maximum number of recent errors to return
            
        Returns:
            List of recent error entries
        """
        try:
            if not self.log_file_path.exists():
                return []
            
            errors = []
            with open(self.log_file_path, 'r') as f:
                for line in f:
                    try:
                        error_entry = json.loads(line.strip())
                        errors.append(error_entry)
                    except json.JSONDecodeError:
                        continue
            
            return errors[-limit:] if errors else []
        except Exception as e:
            self.logger.error(f"Failed to retrieve recent errors: {str(e)}")
            return []


# Global error logger instance
error_logger = EnhancedErrorLogger()


def log_migration_error(*args, **kwargs):
    """Convenience function for logging migration errors."""
    return error_logger.log_migration_error(*args, **kwargs)


def log_program_generation_error(*args, **kwargs):
    """Convenience function for logging program generation errors."""
    return error_logger.log_program_generation_error(*args, **kwargs)


def log_validation_error(*args, **kwargs):
    """Convenience function for logging validation errors."""
    return error_logger.log_validation_error(*args, **kwargs)