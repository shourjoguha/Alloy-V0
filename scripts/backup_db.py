#!/usr/bin/env python3

import os
import sys
import datetime
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """
    Load environment variables from .env file.
    """
    # Look for .env in the current directory or parent directories
    current_dir = Path.cwd()
    env_file = current_dir / '.env'
    
    if not env_file.exists():
        # Try parent directory
        env_file = current_dir.parent / '.env'
    
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded environment from {env_file}")
    else:
        print("Warning: .env file not found. Relying on existing environment variables.")
    
    return {
        'host': os.getenv('DATABASE_HOST', 'localhost'),
        'port': os.getenv('DATABASE_PORT', '5432'),
        'db': os.getenv('DATABASE_NAME', 'Jacked-DB'),
        'user': os.getenv('DATABASE_USER', 'jacked'),
        'password': os.getenv('DATABASE_PASSWORD', 'jackedpass'),
        'container_id': os.getenv('POSTGRES_CONTAINER_ID')
    }

def backup_database():
    """
    Create a backup of the database using pg_dump via Docker.
    """
    config = load_env()
    
    container_id = config.get('container_id')
    if not container_id:
        print("Error: POSTGRES_CONTAINER_ID not found in environment variables.")
        sys.exit(1)
        
    db_name = config['db']
    db_user = config['user']
    
    # Create backups directory if it doesn't exist
    backup_dir = Path.cwd() / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create plain SQL backup (human readable)
    sql_backup_filename = f"{db_name}_backup_{timestamp}.sql"
    sql_backup_path = backup_dir / sql_backup_filename
    
    # Create binary backup (efficient, restore-friendly)
    binary_backup_filename = f"{db_name}_backup_{timestamp}.dump"
    binary_backup_path = backup_dir / binary_backup_filename
    
    print(f"Starting backups for database '{db_name}' from container '{container_id}'...")
    
    # 1. Generate SQL Backup
    print(f"Generating SQL backup...")
    cmd_sql = [
        'docker', 'exec', container_id,
        'pg_dump', '-U', db_user, db_name
    ]
    
    try:
        with open(sql_backup_path, 'w') as f:
            subprocess.run(
                cmd_sql, 
                stdout=f, 
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        print(f"SQL backup saved: {sql_backup_path}")
    except Exception as e:
        print(f"Failed to create SQL backup: {e}")

    # 2. Generate Binary Backup (-Fc)
    print(f"Generating Binary backup (.dump)...")
    # Note: We don't use text=True here because output is binary
    cmd_binary = [
        'docker', 'exec', container_id,
        'pg_dump', '-Fc', '-U', db_user, db_name
    ]
    
    try:
        with open(binary_backup_path, 'wb') as f:
            subprocess.run(
                cmd_binary, 
                stdout=f, 
                stderr=subprocess.PIPE,
                check=True
            )
        
        file_size = binary_backup_path.stat().st_size
        print(f"Binary backup saved: {binary_backup_path}")
        print(f"Binary backup size: {file_size / 1024 / 1024:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating binary backup: {e}")
        # Clean up empty file if failed
        if binary_backup_path.exists() and binary_backup_path.stat().st_size == 0:
            binary_backup_path.unlink()
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    backup_database()
