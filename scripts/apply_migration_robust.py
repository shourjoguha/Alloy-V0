import psycopg2
import os
import sys

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
        port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
        database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
        user=os.environ.get("DB_USER", DEFAULT_DB_USER),
        password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
    )

def apply_migration_robust(sql_file):
    conn = get_db_connection()
    conn.autocommit = True
    cursor = conn.cursor()
    
    with open(sql_file, 'r') as f:
        sql_content = f.read()
        
    # Check for UP/DOWN markers
    up_marker = "-- ==== UP ===="
    down_marker = "-- ==== DOWN ===="
    
    if up_marker in sql_content:
        print(f"Detected UP/DOWN markers in {sql_file}")
        # Extract UP section
        parts = sql_content.split(up_marker)
        if len(parts) > 1:
            up_content = parts[1]
            if down_marker in up_content:
                up_content = up_content.split(down_marker)[0]
            sql_to_run = up_content.strip()
            print("Running UP section...")
        else:
            print("Could not find content after UP marker.")
            return
    else:
        print(f"No UP/DOWN markers found in {sql_file}, running entire file.")
        sql_to_run = sql_content

    print(f"Connected to {conn.dsn}")
    
    try:
        print(f"Executing SQL from {sql_file}...")
        cursor.execute(sql_to_run)
        print("Execution finished.")
        print(f"Status message: {cursor.statusmessage}")
        
        # Verify immediately
        cursor.execute("SELECT current_schema()")
        print(f"Current schema: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_name = 'hyrox_workouts_staging'")
        tables = cursor.fetchall()
        print(f"Verification: Found tables named 'hyrox_workouts_staging': {tables}")
        
        # Check for the new columns
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'hyrox_workouts_staging' 
            AND column_name IN ('total_rounds', 'has_mini_circuit')
        """)
        columns = cursor.fetchall()
        print(f"Verification: Found columns: {columns}")
        
    except psycopg2.Error as e:
        print(f"PostgreSQL Error: {e.pgcode} - {e.pgerror}")
        if hasattr(e, 'diag') and e.diag:
             print(f"Diagnostics: {e.diag.message_primary}")
    except Exception as e:
        print(f"General Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python apply_migration_robust.py <sql_file>")
        sys.exit(1)
    apply_migration_robust(sys.argv[1])
