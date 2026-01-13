import json
import glob
import os

def fix_newlines_in_json():
    # Get absolute path to the project root (parent of scripts dir)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    target_pattern = os.path.join(project_root, "exercises", "questions", "*.json")
    
    files = glob.glob(target_pattern)

    print(f"Searching in: {target_pattern}")
    print(f"Found {len(files)} files to process.")

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding {file_path}: {e}")
                continue

        modified = False
        
        # Iterate over list of problems
        for item in data:
            # Check explanation
            if 'explanation' in item and '<br>' in item['explanation']:
                item['explanation'] = item['explanation'].replace('<br>', '\n')
                modified = True
            
            # Check question (just in case)
            if 'question' in item and '<br>' in item['question']:
                item['question'] = item['question'].replace('<br>', '\n')
                modified = True

        if modified:
            print(f"Fixing <br> in {os.path.basename(file_path)}")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            print(f"No changes needed for {os.path.basename(file_path)}")

if __name__ == '__main__':
    fix_newlines_in_json()
