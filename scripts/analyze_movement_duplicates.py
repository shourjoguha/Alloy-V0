import psycopg2
import json
from difflib import SequenceMatcher

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
cur.execute("SELECT name FROM movements ORDER BY name")
existing_movements = [row[0] for row in cur.fetchall()]

def similarity(str1, str2):
    """Calculate similarity between two strings."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

print("=" * 80)
print("MOVEMENT DUPLICATE ANALYSIS")
print("=" * 80)

print(f"\nHyrox movements: {len(hyrox_movements)}")
print(f"Existing movements: {len(existing_movements)}")

# Exact matches
print("\n" + "=" * 80)
print("EXACT MATCHES")
print("=" * 80)
exact_matches = []
for hyrox in hyrox_movements:
    for existing in existing_movements:
        if hyrox.lower() == existing.lower():
            exact_matches.append((hyrox, existing))
            print(f"✓ EXACT: '{hyrox}' == '{existing}'")

# High similarity matches (> 0.8)
print("\n" + "=" * 80)
print("HIGH SIMILARITY MATCHES (> 0.8)")
print("=" * 80)
high_similarity = []
for hyrox in hyrox_movements:
    for existing in existing_movements:
        if hyrox.lower() != existing.lower():
            sim = similarity(hyrox, existing)
            if sim > 0.8:
                high_similarity.append((hyrox, existing, sim))
                print(f"~ {sim:.2f}: '{hyrox}' ~ '{existing}'")

# Medium similarity matches (0.5 - 0.8)
print("\n" + "=" * 80)
print("MEDIUM SIMILARITY MATCHES (0.5 - 0.8)")
print("=" * 80)
medium_similarity = []
for hyrox in hyrox_movements:
    for existing in existing_movements:
        if hyrox.lower() != existing.lower():
            sim = similarity(hyrox, existing)
            if 0.5 <= sim <= 0.8:
                medium_similarity.append((hyrox, existing, sim))
                print(f"~ {sim:.2f}: '{hyrox}' ~ '{existing}'")

# Substring matches
print("\n" + "=" * 80)
print("SUBSTRING MATCHES")
print("=" * 80)
substring_matches = []
for hyrox in hyrox_movements:
    for existing in existing_movements:
        if hyrox.lower() != existing.lower():
            if hyrox.lower() in existing.lower():
                substring_matches.append((hyrox, existing, "hyrox_in_existing"))
                print(f"⊆ '{hyrox}' IN '{existing}'")
            elif existing.lower() in hyrox.lower():
                substring_matches.append((hyrox, existing, "existing_in_hyrox"))
                print(f"⊆ '{existing}' IN '{hyrox}'")

# Hyrox movements with no close match
print("\n" + "=" * 80)
print("HYROX MOVEMENTS WITH NO CLOSE MATCH (NEW)")
print("=" * 80)
all_matched = set()
for hyrox, existing, _ in high_similarity:
    all_matched.add(hyrox)
for hyrox, existing, _ in medium_similarity:
    all_matched.add(hyrox)
for hyrox, existing, _ in substring_matches:
    all_matched.add(hyrox)
for hyrox, existing in exact_matches:
    all_matched.add(hyrox)

new_movements = [m for m in hyrox_movements if m not in all_matched]
for movement in new_movements:
    print(f"✓ NEW: '{movement}'")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Exact matches: {len(exact_matches)}")
print(f"High similarity matches (> 0.8): {len(set([h for h, e, s in high_similarity]))}")
print(f"Medium similarity matches (0.5-0.8): {len(set([h for h, e, s in medium_similarity]))}")
print(f"Substring matches: {len(set([h for h, e, t in substring_matches]))}")
print(f"New movements (no close match): {len(new_movements)}")

# Save analysis results
analysis = {
    "exact_matches": [{"hyrox": h, "existing": e} for h, e in exact_matches],
    "high_similarity": [{"hyrox": h, "existing": e, "similarity": s} for h, e, s in high_similarity],
    "medium_similarity": [{"hyrox": h, "existing": e, "similarity": s} for h, e, s in medium_similarity],
    "substring_matches": [{"hyrox": h, "existing": e, "type": t} for h, e, t in substring_matches],
    "new_movements": new_movements,
    "summary": {
        "hyrox_count": len(hyrox_movements),
        "existing_count": len(existing_movements),
        "exact_matches": len(exact_matches),
        "high_similarity_count": len(set([h for h, e, s in high_similarity])),
        "medium_similarity_count": len(set([h for h, e, s in medium_similarity])),
        "substring_count": len(set([h for h, e, t in substring_matches])),
        "new_count": len(new_movements)
    }
}

with open('/Users/shourjosmac/Documents/Alloy V0/movement_duplicate_analysis.json', 'w') as f:
    json.dump(analysis, f, indent=2)

print(f"\nAnalysis saved to: movement_duplicate_analysis.json")

cur.close()
conn.close()
