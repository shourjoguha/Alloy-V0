import json
import sys
sys.path.append('/Users/shourjosmac/Documents/Alloy V0/scripts')

from load_hyrox_workouts import HyroxWorkoutLoader

loader = HyroxWorkoutLoader("postgresql://test:test@localhost/test", dry_run=True)

# Read sample data
with open('/Users/shourjosmac/Documents/Alloy V0/hyrox_workouts_sample.json', 'r') as f:
    workouts = json.load(f)

# Debug parsing for first workout
workout = workouts[3]  # telliskivi (has buy-in and cash-out)
print(f"Workout: {workout['name']}")
print(f"Description lines:")
for i, line in enumerate(workout['description_lines'], 1):
    print(f"  {i}. {line}")
    
print("\nParsed lines:")
for i, line in enumerate(workout['description_lines'], 1):
    parsed = loader.parse_workout_line(line, i, 1, False, False)
    if parsed:
        print(f"  {i}. Movement: {parsed.get('movement_name')}")
    else:
        print(f"  {i}. SKIPPED")
