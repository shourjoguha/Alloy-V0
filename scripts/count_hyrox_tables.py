import psycopg2
import os

# DB Config matching scripts/check_tables.py
DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = "5434"
DEFAULT_DB_NAME = "Jacked-DB"
DEFAULT_DB_USER = "jacked"
DEFAULT_DB_PASS = "jackedpass"

def count_hyrox_tables():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST", DEFAULT_DB_HOST),
            port=os.environ.get("DB_PORT", DEFAULT_DB_PORT),
            database=os.environ.get("DB_NAME", DEFAULT_DB_NAME),
            user=os.environ.get("DB_USER", DEFAULT_DB_USER),
            password=os.environ.get("DB_PASS", DEFAULT_DB_PASS)
        )
        cursor = conn.cursor()

        # Query 1: Find all tables starting with 'hyrox_'
        # User asked for: SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'hyrox_%';
        # I'll add schema filter to be safe, usually 'public'
        query_tables = """
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_name LIKE 'hyrox_%'
            AND table_schema = 'public';
        """
        cursor.execute(query_tables)
        tables = cursor.fetchall()

        if not tables:
            print("No tables found starting with 'hyrox_'.")
            return

        print(f"Found {len(tables)} tables. Counting records...")
        print("-" * 50)
        print(f"{'Table Name':<40} | {'Count':<10}")
        print("-" * 50)

        # Query 2: Count records for each table
        for schema, table_name in tables:
            try:
                # Use format for table name, be careful with SQL injection but this is internal script
                query_count = f'SELECT count(*) FROM "{schema}"."{table_name}";'
                cursor.execute(query_count)
                count = cursor.fetchone()[0]
                print(f"{table_name:<40} | {count:<10}")
            except Exception as e:
                print(f"{table_name:<40} | Error: {e}")
                conn.rollback() # Rollback in case of error to proceed to next

        conn.close()

    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    count_hyrox_tables()
