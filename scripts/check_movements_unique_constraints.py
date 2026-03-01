import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_movements_unique_constraints():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD")
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.attname AS column_name
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = 'movements'::regclass
              AND i.indisunique = true
            ORDER BY i.indisprimary DESC, a.attname;
        """)
        
        constraints = cursor.fetchall()
        print("Unique constraints on movements table:")
        for constraint in constraints:
            print(f"  - {constraint[0]}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_movements_unique_constraints()
