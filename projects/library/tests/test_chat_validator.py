"""
Unit Tests for Chat Validator
BugHunter's Test Suite - Ensuring quality! 🛡️🧪
"""

import unittest
import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from chat_validator import ChatValidator


class TestChatValidator(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary chat file for testing"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.temp_file.close()
        self.validator = ChatValidator(self.temp_file.name, max_size_mb=0.001)  # 1KB for testing
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_initial_stats(self):
        """Test initial stats on empty file"""
        stats = self.validator.get_stats()
        self.assertEqual(stats['total_messages'], 0)
        self.assertEqual(stats['file_size_bytes'], 0)
    
    def test_append_message(self):
        """Test appending a message"""
        msg = "**BugHunter**\nTest message content"
        success, status = self.validator.append_message(msg)
        
        self.assertTrue(success)
        self.assertIn("✅", status)
        
        messages = self.validator.read_messages()
        self.assertEqual(len(messages), 1)
        self.assertIn("BugHunter", messages[0])
    
    def test_validate_format(self):
        """Test format validation"""
        # Valid format
        valid_msg = "**Name**\nContent"
        self.assertTrue(self.validator.validate_append_only(valid_msg))
        
        # Invalid format (no bold name)
        invalid_msg = "Just plain text"
        # Should still return True but print warning (we're not strict by default)
        result = self.validator.validate_append_only(invalid_msg)
        # The validator warns but allows it unless force=False in append_message
    
    def test_empty_message(self):
        """Test empty message rejection"""
        success, status = self.validator.append_message("")
        self.assertFalse(success)
        self.assertIn("❌", status)
    
    def test_auto_trim(self):
        """Test auto-trim when exceeding size limit"""
        # Use a very small limit to force trimming
        self.validator = ChatValidator(self.temp_file.name, max_size_mb=0.0001)  # 0.1KB
        
        # Add multiple messages until we exceed limit
        for i in range(10):
            msg = f"**User{i}**\nMessage number {i} with some extra content to make it longer"
            self.validator.append_message(msg)
        
        # Check that old messages were trimmed
        stats = self.validator.get_stats()
        self.assertLessEqual(stats['file_size_bytes'], self.validator.max_size_bytes)
        # Should have fewer than 10 messages due to trimming
        self.assertLess(stats['total_messages'], 10)
    
    def test_multiple_appends(self):
        """Test multiple sequential appends"""
        messages_to_add = [
            "**Alice**\nHello everyone!",
            "**Bob**\nHi Alice!",
            "**Charlie**\nHey folks!"
        ]
        
        for msg in messages_to_add:
            success, _ = self.validator.append_message(msg)
            self.assertTrue(success)
        
        all_messages = self.validator.read_messages()
        self.assertEqual(len(all_messages), 3)
        self.assertIn("Alice", all_messages[0])
        self.assertIn("Bob", all_messages[1])
        self.assertIn("Charlie", all_messages[2])


class TestChatValidatorIntegration(unittest.TestCase):
    """Integration tests with actual Chat.txt"""
    
    def test_with_real_chat_file(self):
        """Test with the actual Chat.txt if it exists"""
        chat_file = 'Chat.txt'
        if not os.path.exists(chat_file):
            self.skipTest("Chat.txt not found")
        
        validator = ChatValidator(chat_file, max_size_mb=1.0)
        stats = validator.get_stats()
        
        # Just verify we can read stats without error
        self.assertIn('total_messages', stats)
        self.assertIn('file_size_mb', stats)
        print(f"\n📊 Real Chat.txt Stats: {stats['total_messages']} messages, {stats['file_size_mb']:.2f} MB")


if __name__ == '__main__':
    print("🛡️  BugHunter's Test Suite Running...")
    print("=" * 50)
    unittest.main(verbosity=2)
