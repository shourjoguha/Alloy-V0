
import psycopg2
import sys
import os

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

def run_migration(sql_file):
    conn = get_db_connection()
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        with open(sql_file, 'r') as f:
            sql = f.read()
        cursor.execute(sql)
        print(f"Migration {sql_file} applied successfully.")
    except Exception as e:
        print(f"Error applying migration: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python apply_migration.py <sql_file>")
        sys.exit(1)
    run_migration(sys.argv[1])
