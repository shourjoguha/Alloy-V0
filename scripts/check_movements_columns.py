import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Check the movements table columns
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'movements' 
    ORDER BY ordinal_position;
""")

print("Movements table columns:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

cur.close()
conn.close()
