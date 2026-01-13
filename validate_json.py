import json
import glob
import os

files = glob.glob("exercises/questions/*.json")
errors = []

for f in files:
    try:
        with open(f, 'r') as fp:
            data = json.load(fp)
            # Check structure
            if not isinstance(data, list):
                errors.append(f"{f}: Root is not a list")
                continue
            for i, item in enumerate(data):
                if "id" not in item:
                    errors.append(f"{f} item {i}: Missing id")
                if "options" in item and len(item["options"]) != 5:
                    # Not strictly an error but worth noting if inconsistent
                    pass
    except json.JSONDecodeError as e:
        errors.append(f"{f}: JSON Error - {e}")

if errors:
    print("Found errors:")
    for e in errors:
        print(e)
else:
    print("All JSON files are valid.")
