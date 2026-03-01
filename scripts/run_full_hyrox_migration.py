import os
import psycopg2
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Migration files in order
MIGRATION_FILES = [
    "hyrox/01_validate_hyrox_staging_data.sql",
    "hyrox/02_create_hyrox_production_tables.sql",
    "hyrox/03_migrate_hyrox_staging_to_production.sql",
    "hyrox/04_create_ancillary_records.sql"
]

def run_migrations():
    conn = None
    try:
        # Connect directly to DB (Bypasses Docker process spawning)
        host = os.getenv("DATABASE_HOST", "localhost")
        port = os.getenv("DATABASE_PORT", "5434")
        dbname = os.getenv("DATABASE_NAME", "Jacked-DB")
        user = os.getenv("DATABASE_USER", "jacked")
        password = os.getenv("DATABASE_PASSWORD", "jackedpass")
        
        logger.info(f"Connecting to {dbname} at {host}:{port} as {user}...")
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=dbname,
            user=user,
            password=password
        )
        conn.autocommit = True # Enable autocommit to handle scripts with internal transactions
        cursor = conn.cursor()
        
        # Base path is the project root (parent of 'scripts' directory)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        logger.info(f"Project root determined as: {base_path}")
        logger.info("🚀 Starting Hyrox Migration (Direct Connection Mode)...")

        # 1. Cleanup incorrect tables if needed (based on schema mismatch diagnosis)
        logger.info("🧹 Cleaning up incorrect production tables...")
        try:
            cursor.execute("DROP TABLE IF EXISTS hyrox_workouts CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS hyrox_workout_lines CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS hyrox_workout_tags CASCADE;")
            cursor.execute("DROP TABLE IF EXISTS hyrox_scraping_log CASCADE;")
            logger.info("✅ Dropped existing production tables.")
        except Exception as e:
            logger.error(f"⚠️ Warning during cleanup: {e}")

        for sql_file in MIGRATION_FILES:
            file_path = os.path.join(base_path, sql_file)
            
            logger.info(f"📜 Processing: {sql_file}")
            
            if not os.path.exists(file_path):
                logger.error(f"❌ File not found: {file_path}")
                continue

            with open(file_path, 'r') as f:
                sql_content = f.read()
                
            try:
                cursor.execute(sql_content)
                logger.info(f"✅ Success: {sql_file}")
            except Exception as e:
                logger.error(f"❌ Failed: {sql_file}")
                logger.error(f"Error details: {e}")
                # We continue to next file or return? 
                # Original script used `set -e` (exit on error).
                return

        logger.info("🎉 All migrations completed successfully!")

    except Exception as e:
        logger.error(f"CRITICAL DB ERROR: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_migrations()
