import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Unmapped movements
unmapped = [
    '20 sandbag lunges',
    '30 sandbag lunges',
    '60 sandbag lunges',
    'Lunges',
    'Row'
]

print("Searching for matches in movements table:")
print("=" * 80)

for movement in unmapped:
    base_name = movement.split()[0] if ' ' in movement else movement
    print(f"\nSearching for: {movement} (base: {base_name})")
    
    # Search for partial matches
    cur.execute("""
        SELECT name, id
        FROM movements
        WHERE name ILIKE %s
        ORDER BY name
        LIMIT 10
    """, (f'%{base_name}%',))
    
    results = cur.fetchall()
    if results:
        print("  Potential matches:")
        for name, id in results:
            print(f"    - {name} (ID: {id})")
    else:
        print("  No matches found")

cur.close()
conn.close()
