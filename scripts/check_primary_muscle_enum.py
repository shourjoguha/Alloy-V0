import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_primary_muscle_enum():
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
            SELECT enumlabel 
            FROM pg_enum 
            WHERE enumtypid = (
                SELECT oid FROM pg_type WHERE typname = 'primarymuscle'
            )
            ORDER BY enumsortorder;
        """)
        
        enum_values = cursor.fetchall()
        print("Valid primarymuscle ENUM values:")
        for value in enum_values:
            print(f"  - {value[0]}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_primary_muscle_enum()
