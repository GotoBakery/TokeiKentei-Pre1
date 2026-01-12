import os

def format_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    inside_math_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_math_marker = (stripped == '$$')
        is_header = line.lstrip().startswith('#')
        
        # Opening Math Block
        if is_math_marker and not inside_math_block:
            # Ensure blank line before
            if new_lines and new_lines[-1].strip() != '':
                new_lines.append('\n')
            new_lines.append(line)
            inside_math_block = True
            continue
            
        # Closing Math Block
        if is_math_marker and inside_math_block:
            new_lines.append(line)
            # Ensure blank line after (will be handled by next iteration logic? No, easier to append here)
            # But we must be careful not to double add if next line is already blank.
            # Let's peek next line? Or just append a blank marker and handle duplicates later?
            # Easier: Just set state. The "Blank line after" is actually "Blank line before the NEXT content".
            # But the next content might be the end of the file.
            inside_math_block = False
            # We want to force a blank line after this closing marker.
            # But we can't easily peek ahead comfortably in this loop structure if we just append.
            # Let's add a flag "just_closed_math"
            continue
            
        # Header
        if is_header:
            # Ensure blank line before
            if new_lines and new_lines[-1].strip() != '':
                new_lines.append('\n')
            new_lines.append(line)
            continue
            
        # Normal line
        # If we just closed a math block, we should ensure this line is preceded by a blank, UNLESS this line is blank itself.
        # But wait, if I check "previous line in new_lines", I can enforce it.
        
        # Let's handle the "Blank line after closing $$" by checking the previous line in new_lines
        if new_lines and new_lines[-1].strip() == '$$':
             # Previous was math marker. Was it closing?
             # Since we track inside_math_block, at this point inside_math_block is True or False.
             # If we are processing a normal line, and previous line was '$$', check if we are inside or outside.
             if not inside_math_block:
                 # We are outside, so the previous '$$' was a closing one.
                 if stripped != '':
                     new_lines.append('\n')

        new_lines.append(line)

    return new_lines


notes_dir = '/workspaces/TokeiKentei-Pre1/notes'
for filename in os.listdir(notes_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(notes_dir, filename)
        formatted_lines = format_file(filepath)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(formatted_lines)
        print(f"Formatted {filepath}")

