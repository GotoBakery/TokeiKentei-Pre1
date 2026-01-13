import json
import glob
import sys

def validate_json_files():
    files = glob.glob('exercises/questions/*.json')
    error_count = 0
    
    print(f"Validating {len(files)} JSON files...")
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                print(f"Error: {file_path} is not a list of questions.")
                error_count += 1
                continue
                
            for i, item in enumerate(data):
                required_keys = ['id', 'type', 'question', 'options', 'answer', 'explanation']
                missing_keys = [k for k in required_keys if k not in item]
                if missing_keys:
                    print(f"Error in {file_path} item {i}: Missing keys {missing_keys}")
                    error_count += 1
                    
        except json.JSONDecodeError as e:
            print(f"JSON Error in {file_path}: {e}")
            error_count += 1
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            error_count += 1
            
    if error_count == 0:
        print("All JSON files are valid.")
    else:
        print(f"Found {error_count} errors.")
        sys.exit(1)

if __name__ == '__main__':
    validate_json_files()
