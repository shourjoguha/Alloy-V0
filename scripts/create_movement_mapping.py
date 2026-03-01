import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    port=5434,
    database="Jacked-DB",
    user="jacked",
    password="jackedpass"
)

cur = conn.cursor()

# Get unique movement names from Hyrox staging
cur.execute("""
    SELECT DISTINCT movement_name
    FROM hyrox_workout_lines_staging
    WHERE movement_name IS NOT NULL
    ORDER BY movement_name
""")
hyrox_movements = [row[0] for row in cur.fetchall()]

# Get existing movements from database
cur.execute("SELECT id, name FROM movements ORDER BY name")
existing_movements = {row[1]: row[0] for row in cur.fetchall()}

# Create mapping based on analysis
movement_mapping = {}

# Exact matches
exact_matches = {
    'Burpees': 'Burpees',
    'Farmer\'s carry': 'Farmer\'S Carry',
    'Rest': 'Rest',
    'Run': 'Run'
}

# High similarity matches
high_similarity = {
    '20 burpees': 'Burpees',
    '30 burpees': 'Burpees',
    '30 hand release push-ups': 'Hand Release Push Ups',
    '5 burpees': 'Burpees',
    'Burpees': 'Burpee'  # Singular form
}

# Substring matches (most reliable)
substring_matches = {
    '10 burpee broad jumps': 'Broad Jump',  # Contains 'Broad Jump'
    '10 wall ball shots': 'Wall Ball',  # Contains 'Wall Ball'
    '20 burpees': 'Burpees',  # Contains 'Burpees'
    '20 push-ups': 'Push-Up',  # Contains 'Push-Up'
    '20 sandbag lunges': 'Lunges',  # Contains 'Lunges'
    '25 sit-ups': '3/4 Sit-Up',  # Contains 'Sit-Up'
    '30 burpees': 'Burpees',  # Contains 'Burpees'
    '30 hand release push-ups': 'Hand Release Push Ups',  # Contains 'Hand Release Push Ups'
    '30 sandbag lunges': 'Lunges',  # Contains 'Lunges'
    '30 wall ball shots': 'Wall Ball',  # Contains 'Wall Ball'
    '40 wall ball shots': 'Wall Ball',  # Contains 'Wall Ball'
    '5 burpees': 'Burpees',  # Contains 'Burpees'
    '60 sandbag lunges': 'Lunges',  # Contains 'Lunges'
    '100 sit-ups': '3/4 Sit-Up',  # Contains 'Sit-Up'
    'Lunges': 'Lunges',  # Exact match (case difference)
    'Calorie ski erg': 'Calorie Row',  # High similarity 0.69
    'V-ups': '3/4 Sit-Up',  # Best match for ab movement
    'Wall ball shots': 'Wall Ball'  # Contains 'Wall Ball'
}

# Combine all mappings (priority: exact > high similarity > substring)
for hyrox, existing in exact_matches.items():
    if hyrox in hyrox_movements:
        movement_mapping[hyrox] = existing

for hyrox, existing in high_similarity.items():
    if hyrox in hyrox_movements and hyrox not in movement_mapping:
        movement_mapping[hyrox] = existing

for hyrox, existing in substring_matches.items():
    if hyrox in hyrox_movements and hyrox not in movement_mapping:
        movement_mapping[hyrox] = existing

# Create final mapping with movement IDs
final_mapping = {}
for hyrox, existing in movement_mapping.items():
    if existing in existing_movements:
        final_mapping[hyrox] = {
            'hyrox_movement': hyrox,
            'existing_movement': existing,
            'movement_id': existing_movements[existing]
        }
    else:
        print(f"WARNING: Existing movement '{existing}' not found in database")

print("=" * 80)
print("MOVEMENT MAPPING")
print("=" * 80)
print(f"Total Hyrox movements: {len(hyrox_movements)}")
print(f"Mapped movements: {len(final_mapping)}")
print(f"Unmapped movements: {len(hyrox_movements) - len(final_mapping)}")

if len(hyrox_movements) - len(final_mapping) > 0:
    print("\nUnmapped movements:")
    for movement in hyrox_movements:
        if movement not in final_mapping:
            print(f"  - {movement}")

print("\nMapped movements:")
for hyrox, mapping in final_mapping.items():
    print(f"  '{hyrox}' -> '{mapping['existing_movement']}' (ID: {mapping['movement_id']})")

# Save mapping to file
with open('/Users/shourjosmac/Documents/Alloy V0/movement_mapping.json', 'w') as f:
    json.dump(final_mapping, f, indent=2)

print(f"\nMapping saved to: movement_mapping.json")

cur.close()
conn.close()
