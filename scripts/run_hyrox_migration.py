import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD")
        )
        cursor = conn.cursor()
        
        with open('/Users/shourjosmac/Documents/Alloy V0/migrations/20260228_add_hyrox_movements.sql', 'r') as f:
            migration_sql = f.read()
        
        cursor.execute(migration_sql)
        conn.commit()
        print("Migration executed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_migration()
