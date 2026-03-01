import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Check workouts
cur.execute("SELECT COUNT(*) FROM hyrox_workouts_staging")
workout_count = cur.fetchone()[0]
print(f"Total workouts: {workout_count}")

# Check workout lines
cur.execute("SELECT COUNT(*) FROM hyrox_workout_lines_staging")
line_count = cur.fetchone()[0]
print(f"Total workout lines: {line_count}")

# Check mini circuits
cur.execute("SELECT COUNT(*) FROM hyrox_mini_circuits_staging")
circuit_count = cur.fetchone()[0]
print(f"Total mini circuits: {circuit_count}")

# Check tags
cur.execute("SELECT COUNT(*) FROM hyrox_workout_tags_staging")
tag_count = cur.fetchone()[0]
print(f"Total tags: {tag_count}")

# Get unique movement names
cur.execute("""
    SELECT DISTINCT movement_name
    FROM hyrox_workout_lines_staging
    WHERE movement_name IS NOT NULL
    ORDER BY movement_name
""")
movements = [row[0] for row in cur.fetchall()]
print(f"\nUnique movements ({len(movements)}):")
for movement in movements:
    print(f"  - {movement}")

# Check if movements table exists and compare
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'movements'
    )
""")
movements_table_exists = cur.fetchone()[0]

if movements_table_exists:
    cur.execute("SELECT name FROM movements ORDER BY name")
    existing_movements = [row[0] for row in cur.fetchall()]
    print(f"\nExisting movements in database ({len(existing_movements)}):")
    for movement in existing_movements:
        print(f"  - {movement}")
    
    # Find potential duplicates
    print("\nPotential duplicates (similar names):")
    for hyrox_movement in movements:
        for existing_movement in existing_movements:
            similarity = len(set(hyrox_movement.lower().split()) & set(existing_movement.lower().split()))
            if similarity >= 2 or hyrox_movement.lower() in existing_movement.lower() or existing_movement.lower() in hyrox_movement.lower():
                print(f"  Hyrox: '{hyrox_movement}' ~ Existing: '{existing_movement}'")

cur.close()
conn.close()
