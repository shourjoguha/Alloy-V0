
import psycopg2
import os

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def check_columns():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
        port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
        database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
        user=os.environ.get("DB_USER", DEFAULT_DB_USER),
        password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'hyrox_mini_circuits_staging';
    """)
    cols = cursor.fetchall()
    print("Columns in hyrox_mini_circuits_staging:")
    for c in cols:
        print(f"- {c[0]} ({c[1]})")
    conn.close()

if __name__ == "__main__":
    check_columns()
