#!/usr/bin/env python3

import os
import sys
import hashlib
from pathlib import Path
from dotenv import load_dotenv
import subprocess

def load_env():
    script_dir = Path(__file__).parent
    env_file = script_dir / '.env'
    parent_env_file = script_dir.parent / '.env'
    
    if parent_env_file.exists():
        load_dotenv(parent_env_file)
    
    return {
        'host': os.getenv('DATABASE_HOST', 'localhost'),
        'port': os.getenv('DATABASE_PORT', '5432'),
        'db': os.getenv('DATABASE_NAME', 'Jacked-DB'),
        'user': os.getenv('DATABASE_USER', 'jacked'),
        'password': os.getenv('DATABASE_PASSWORD', 'jackedpass'),
        'container_id': os.getenv('POSTGRES_CONTAINER_ID')
    }

def get_migration_file_checksum(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return hashlib.md5(content.encode()).hexdigest()

def get_current_migration_version(db_config):
    psql_cmd = [
        'docker', 'exec', db_config['container_id'],
        'psql', '-U', db_config['user'], '-d', db_config['db'],
        '-t', '-c',
        "SELECT version FROM migration_version ORDER BY applied_at DESC LIMIT 1;"
    ]
    result = subprocess.run(psql_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        version = result.stdout.strip()
        return version if version else None
    return None

def is_migration_applied(db_config, checksum):
    psql_cmd = [
        'docker', 'exec', db_config['container_id'],
        'psql', '-U', db_config['user'], '-d', db_config['db'],
        '-t', '-c',
        f"SELECT EXISTS(SELECT 1 FROM migration_version WHERE checksum = '{checksum}');"
    ]
    result = subprocess.run(psql_cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip().lower() == 't'
    return False

def apply_migration(db_config, migration_file):
    with open(migration_file, 'r') as f:
        sql_content = f.read()
    
    checksum = hashlib.md5(sql_content.encode()).hexdigest()
    
    print(f"Applying migration: {migration_file}")
    print(f"Checksum: {checksum}")
    
    psql_cmd = [
        'docker', 'exec', '-i', db_config['container_id'],
        'psql', '-U', db_config['user'], '-d', db_config['db']
    ]
    
    process = subprocess.Popen(
        psql_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=sql_content)
    
    if process.returncode != 0:
        print(f"ERROR: Migration failed")
        print(f"STDOUT: {stdout}")
        print(f"STDERR: {stderr}")
        return False
    
    import datetime
    version = f"{migration_file.stem}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    psql_insert_cmd = [
        'docker', 'exec', db_config['container_id'],
        'psql', '-U', db_config['user'], '-d', db_config['db'],
        '-c', f"INSERT INTO migration_version (version, description, checksum) VALUES ('{version}', '{migration_file}', '{checksum}');"
    ]
    
    subprocess.run(psql_insert_cmd, check=True)
    
    print("Migration applied successfully!")
    show_migration_status(db_config)
    return True

def show_migration_status(db_config):
    psql_cmd = [
        'docker', 'exec', db_config['container_id'],
        'psql', '-U', db_config['user'], '-d', db_config['db'],
        '-c', "SELECT version, description, applied_at FROM migration_version ORDER BY applied_at DESC;"
    ]
    subprocess.run(psql_cmd)

def main():
    db_config = load_env()
    script_dir = Path(__file__).parent
    migration_file = script_dir / 'migrations.sql'
    
    if not migration_file.exists():
        print(f"ERROR: Migration file {migration_file} not found")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'status':
            print("Current migration status:")
            show_migration_status(db_config)
            return
        
        elif command == 'apply':
            checksum = get_migration_file_checksum(migration_file)
            
            if is_migration_applied(db_config, checksum):
                print("Migration already applied (matching checksum)")
                show_migration_status(db_config)
                return
            
            success = apply_migration(db_config, migration_file)
            sys.exit(0 if success else 1)
        
        else:
            print(f"Unknown command: {command}")
            print("Usage: python migrate.py [status|apply]")
            sys.exit(1)
    else:
        print("Usage: python migrate.py [status|apply]")
        print("\nCommands:")
        print("  status  - Show current migration status")
        print("  apply   - Apply migrations.sql file")
        sys.exit(0)

if __name__ == '__main__':
    main()
