import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Drop existing tables in correct order (respecting FKs)
cur.execute("DROP TABLE IF EXISTS hyrox_workout_lines_staging CASCADE")
cur.execute("DROP TABLE IF EXISTS hyrox_mini_circuits_staging CASCADE")
cur.execute("DROP TABLE IF EXISTS hyrox_time_segments_staging CASCADE")
cur.execute("DROP TABLE IF EXISTS hyrox_ladder_rungs_staging CASCADE")
cur.execute("DROP TABLE IF EXISTS hyrox_workout_tags_staging CASCADE")
cur.execute("DROP TABLE IF EXISTS hyrox_workouts_staging CASCADE")

# Drop existing types
cur.execute("DROP TYPE IF EXISTS hyrox_workout_type CASCADE")
cur.execute("DROP TYPE IF EXISTS hyrox_workout_goal CASCADE")
cur.execute("DROP TYPE IF EXISTS hyrox_status CASCADE")

conn.commit()
print("Dropped all existing Hyrox tables and types")
cur.close()
conn.close()
