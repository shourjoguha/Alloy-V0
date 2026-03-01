#!/usr/bin/env python3
import subprocess
import sys

# Run the add_hyrox_movements.py script
result = subprocess.run([sys.executable, 'scripts/add_hyrox_movements.py'], capture_output=True, text=True, cwd='/Users/shourjosmac/Documents/Alloy V0')

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")

sys.exit(result.returncode)
