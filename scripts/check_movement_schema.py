import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Check the pattern column type
cur.execute("""
    SELECT column_name, data_type, udt_name 
    FROM information_schema.columns 
    WHERE table_name = 'movements' 
      AND column_name = 'pattern'
""")

print("Pattern column info:")
for row in cur.fetchall():
    print(f"  Column: {row[0]}")
    print(f"  Data type: {row[1]}")
    print(f"  UDT name: {row[2]}")

cur.close()
conn.close()
