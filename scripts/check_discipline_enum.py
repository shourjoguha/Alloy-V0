import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Check the enum type
cur.execute("""
    SELECT enumlabel 
    FROM pg_enum 
    WHERE enumtypid = (
        SELECT oid FROM pg_type WHERE typname = 'disciplinetype_new3'
    )
    ORDER BY enumsortorder;
""")

print("Valid discipline values:")
for row in cur.fetchall():
    print(f"  - {row[0]}")

cur.close()
conn.close()
