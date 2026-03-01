
import psycopg2
import os

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def check_tables():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
        port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
        database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
        user=os.environ.get("DB_USER", DEFAULT_DB_USER),
        password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'hyrox%';
    """)
    tables = cursor.fetchall()
    print("Existing Hyrox tables:")
    for t in tables:
        print(f"- {t[0]}")
    
    try:
        cursor.execute("SELECT count(*) FROM hyrox_workouts_staging")
        print(f"hyrox_workouts_staging count: {cursor.fetchone()[0]}")
    except Exception as e:
        print(f"Error querying hyrox_workouts_staging: {e}")
        
    conn.close()

if __name__ == "__main__":
    check_tables()
