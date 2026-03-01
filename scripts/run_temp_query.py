import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", "5434")
DB_NAME = os.getenv("DATABASE_NAME", "Jacked-DB")
DB_USER = os.getenv("DATABASE_USER", "jacked")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD", "jackedpass")

def run_query():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        query = """
        SELECT id, name, workout_type, full_description, total_rounds 
        FROM hyrox_workouts_staging 
        WHERE workout_type::text LIKE 'rounds_for_%' AND total_rounds IS NULL 
        LIMIT 10;
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        if not rows:
            print("No results found.")
        else:
            print(f"{'ID':<38} | {'Name':<30} | {'Type':<20} | {'Rounds':<10} | {'Description'}")
            print("-" * 150)
            for row in rows:
                # Truncate description for display
                desc = row[3] if row[3] else ""
                if len(desc) > 50:
                    desc = desc[:47] + "..."
                
                print(f"{str(row[0]):<38} | {row[1][:30]:<30} | {row[2]:<20} | {str(row[4]):<10} | {desc}")
                
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_query()
