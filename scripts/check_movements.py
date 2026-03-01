
import psycopg2
import os

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def check_movements():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
            port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
            database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
            user=os.environ.get("DB_USER", DEFAULT_DB_USER),
            password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
        )
        cursor = conn.cursor()
        
        movements = ['Burpee Broad Jumps', 'Calorie Ski Erg', 'V-Ups', 'Sit-Ups', 'Sandbag Lunges', 'Lunges']
        cursor.execute("SELECT name FROM movements WHERE name IN %s", (tuple(movements),))
        found = cursor.fetchall()
        print(f"Found movements: {[m[0] for m in found]}")
        
        conn.close()
    except Exception as e:
        print(f"Error checking movements: {e}")

if __name__ == "__main__":
    check_movements()
