
import psycopg2
import os
import sys

# Default connection params matching existing scripts
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
            port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
            database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
            user=os.environ.get("DB_USER", DEFAULT_DB_USER),
            password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def verify_fixes():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("==================================================")
    print("VERIFYING HYROX STAGING FIXES")
    print("==================================================\n")

    # 1. Count lines with is_rest=true
    print("1. Checking 'is_rest=true' count in hyrox_workout_lines_staging...")
    cursor.execute("SELECT count(*) FROM hyrox_workout_lines_staging WHERE is_rest = true;")
    rest_count = cursor.fetchone()[0]
    print(f"   Result: {rest_count} lines found with is_rest=true.\n")

    # 2. Check for mixed metrics
    print("2. Checking for mixed metrics (reps AND (distance OR calories OR duration))...")
    cursor.execute("""
        SELECT count(*) 
        FROM hyrox_workout_lines_staging 
        WHERE reps IS NOT NULL 
          AND (distance_meters IS NOT NULL OR calories IS NOT NULL OR duration_seconds IS NOT NULL);
    """)
    mixed_count = cursor.fetchone()[0]
    status = "PASS" if mixed_count == 0 else "FAIL"
    print(f"   Result: {mixed_count} rows found. [{status}] (Expected: 0)\n")

    # 3. Check for movement names starting with a digit
    print("3. Checking for movement names starting with a digit...")
    cursor.execute("""
        SELECT count(*) 
        FROM hyrox_workout_lines_staging 
        WHERE movement_name ~ '^[0-9]';
    """)
    digit_start_count = cursor.fetchone()[0]
    status = "PASS" if digit_start_count == 0 else "FAIL"
    print(f"   Result: {digit_start_count} rows found. [{status}] (Expected: 0)\n")
    
    if digit_start_count > 0:
        cursor.execute("""
            SELECT movement_name 
            FROM hyrox_workout_lines_staging 
            WHERE movement_name ~ '^[0-9]'
            LIMIT 5;
        """)
        bad_examples = cursor.fetchall()
        print(f"   Examples: {[b[0] for b in bad_examples]}\n")

    # 4. Check for rounds in mini circuits
    print("4. Checking for rows where 'rounds' is NOT NULL in hyrox_mini_circuits_staging...")
    cursor.execute("""
        SELECT count(*) 
        FROM hyrox_mini_circuits_staging 
        WHERE rounds IS NOT NULL;
    """)
    rounds_count = cursor.fetchone()[0]
    print(f"   Result: {rounds_count} rows found with rounds specified.\n")

    # 5. List distinct movement_name values
    print("5. Listing distinct movement_name values (for visual check):")
    cursor.execute("""
        SELECT DISTINCT movement_name 
        FROM hyrox_workout_lines_staging 
        WHERE movement_name IS NOT NULL
        ORDER BY movement_name;
    """)
    movements = cursor.fetchall()
    if not movements:
        print("   No movements found.")
    else:
        print(f"   Found {len(movements)} distinct movements:")
        for m in movements:
            print(f"   - {m[0]}")
    print("")

    # 6. Check if hyrox_workout_tags_staging exists
    print("6. Checking if 'hyrox_workout_tags_staging' table exists...")
    cursor.execute("SELECT to_regclass('public.hyrox_workout_tags_staging');")
    table_exists = cursor.fetchone()[0]
    status = "PASS" if table_exists is None else "FAIL"
    print(f"   Result: {table_exists} [{status}] (Expected: None/False)\n")

    conn.close()
    print("==================================================")
    print("VERIFICATION COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    verify_fixes()
