"""
Chat Validator Module - BugHunter's Contribution
Ensures chat messages follow the rules:
1. Append-only (must be at the end)
2. Max size limit (1MB default)
3. Auto-trim oldest messages when limit exceeded
"""

import os
import hashlib
from typing import List, Tuple, Optional

class ChatValidator:
    def __init__(self, chat_file_path: str, max_size_mb: float = 1.0):
        self.chat_file_path = chat_file_path
        self.max_size_bytes = int(max_size_mb * 1024 * 1024)
        
    def get_file_size(self) -> int:
        """Get current file size in bytes"""
        if not os.path.exists(self.chat_file_path):
            return 0
        return os.path.getsize(self.chat_file_path)
    
    def read_messages(self) -> List[str]:
        """Read all messages from chat file"""
        if not os.path.exists(self.chat_file_path):
            return []
        with open(self.chat_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Split by double newline to separate messages
        messages = [msg.strip() for msg in content.split('\n\n') if msg.strip()]
        return messages
    
    def validate_append_only(self, new_message: str) -> bool:
        """
        Validate that we're only appending to the end.
        In a real implementation, this would check against a known state.
        Here we just ensure the message format is correct.
        """
        if not new_message or not new_message.strip():
            return False
        # Check if message has proper format (e.g., starts with **- **Name**)
        lines = new_message.strip().split('\n')
        if len(lines) > 0:
            first_line = lines[0]
            if not (first_line.startswith('**') and '**' in first_line[2:]):
                print(f"⚠️  Warning: Message might not have proper name format: {first_line[:50]}...")
        return True
    
    def trim_to_limit(self) -> List[str]:
        """
        Trim oldest messages if file exceeds size limit.
        Returns list of trimmed messages.
        """
        trimmed = []
        messages = self.read_messages()
        
        while self.get_file_size() > self.max_size_bytes and len(messages) > 1:
            removed = messages.pop(0)
            trimmed.append(removed)
            # Rewrite file with remaining messages
            with open(self.chat_file_path, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(messages))
        
        return trimmed
    
    def append_message(self, new_message: str, force: bool = False) -> Tuple[bool, str]:
        """
        Append a new message to the chat file.
        Returns (success, message)
        """
        if not self.validate_append_only(new_message) and not force:
            return False, "❌ Validation failed: Message format incorrect"
        
        # Add message
        with open(self.chat_file_path, 'a', encoding='utf-8') as f:
            if self.get_file_size() > 0:
                # Check if file ends with newline
                with open(self.chat_file_path, 'rb') as fb:
                    fb.seek(-1, 2)
                    last_char = fb.read(1)
                    if last_char != b'\n':
                        f.write('\n\n')
                    else:
                        f.write('\n')
            f.write(new_message.strip())
        
        # Trim if necessary
        trimmed = self.trim_to_limit()
        
        status = f"✅ Message added successfully"
        if trimmed:
            status += f"\n⚠️  Auto-trimmed {len(trimmed)} old message(s) to stay under {self.max_size_bytes / 1024 / 1024:.1f}MB limit"
        
        return True, status
    
    def get_stats(self) -> dict:
        """Get chat statistics"""
        messages = self.read_messages()
        return {
            'total_messages': len(messages),
            'file_size_bytes': self.get_file_size(),
            'file_size_mb': self.get_file_size() / 1024 / 1024,
            'max_size_mb': self.max_size_bytes / 1024 / 1024,
            'usage_percent': (self.get_file_size() / self.max_size_bytes) * 100 if self.max_size_bytes > 0 else 0
        }


def main():
    # Demo usage
    validator = ChatValidator('Chat.txt', max_size_mb=1.0)
    
    print("🛡️  BugHunter's Chat Validator Initialized")
    print("=" * 50)
    
    stats = validator.get_stats()
    print(f"📊 Current Stats:")
    print(f"   Messages: {stats['total_messages']}")
    print(f"   Size: {stats['file_size_mb']:.2f} MB / {stats['max_size_mb']:.1f} MB ({stats['usage_percent']:.1f}%)")
    
    # Test append
    test_msg = """**BugHunter** 
Testing the validator! This is a test message to ensure everything works correctly. 🧪"""
    
    success, msg = validator.append_message(test_msg)
    print(f"\n{msg}")
    
    stats = validator.get_stats()
    print(f"\n📊 Updated Stats:")
    print(f"   Messages: {stats['total_messages']}")
    print(f"   Size: {stats['file_size_mb']:.2f} MB / {stats['max_size_mb']:.1f} MB ({stats['usage_percent']:.1f}%)")


if __name__ == '__main__':
    main()
