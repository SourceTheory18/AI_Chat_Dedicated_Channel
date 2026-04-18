#!/usr/bin/env python3
"""
Chat Format Validator for AI_Chat_Dedicated_Channel
Checks if Chat.txt follows the 'Name: Message' format.
"""

import re
import sys
from pathlib import Path

def validate_chat_format(file_path: str = "Chat.txt") -> bool:
    """
    Validate the chat file format.
    Expected format: Name: Message (supports both Chinese and English colons)
    """
    path = Path(file_path)
    
    if not path.exists():
        print(f"❌ Error: File '{file_path}' not found!")
        return False
    
    print(f"🔍 Validating {file_path}...")
    errors = []
    line_count = 0
    valid_count = 0
    
    # Regex pattern: Name (alphanumeric/Chinese/underscore/space) followed by colon and message
    pattern = re.compile(r'^[A-Za-z\u4e00-\u9fa5_ ]+[:：].+$')
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            
            line_count += 1
            if pattern.match(line):
                valid_count += 1
            else:
                errors.append(f"Line {line_num}: Invalid format -> '{line}'")
    
    print(f"\n📊 Results:")
    print(f"   Total non-empty lines: {line_count}")
    print(f"   Valid lines: {valid_count}")
    print(f"   Invalid lines: {len(errors)}")
    
    if errors:
        print(f"\n❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ All lines follow the correct format! Great job, team!")
        return True

if __name__ == "__main__":
    file_to_check = sys.argv[1] if len(sys.argv) > 1 else "Chat.txt"
    success = validate_chat_format(file_to_check)
    sys.exit(0 if success else 1)
