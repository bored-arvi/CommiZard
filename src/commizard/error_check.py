"""
Test suite for Ollama error handling functionality.

Run from the CommiZard root directory with:
    python -m pytest src/commizard/test_ollama_errors.py -v
Or:
    cd src/commizard && python test_ollama_errors.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the commizard package to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the error handler
try:
    from ollama_errors import get_error_message
except ImportError:
    print("ERROR: Could not import ollama_errors. Make sure ollama_errors.py exists in the same directory.")
    sys.exit(1)


class TestOllamaErrors(unittest.TestCase):
    """Test cases for ollama_errors.get_error_message()"""
    
    def test_400_bad_request(self):
        """Test 400 Bad Request error message"""
        result = get_error_message(400)
        self.assertIn("Error 400", result)
        self.assertIn("Bad Request", result)
        self.assertIn("malformed", result)
        self.assertIn("Suggestions", result)
        
    def test_403_forbidden(self):
        """Test 403 Forbidden error message"""
        result = get_error_message(403)
        self.assertIn("Error 403", result)
        self.assertIn("Forbidden", result)
        self.assertIn("OLLAMA_ORIGINS", result)
        
    def test_404_not_found(self):
        """Test 404 Not Found error message"""
        result = get_error_message(404)
        self.assertIn("Error 404", result)
        self.assertIn("Model Not Found", result)
        self.assertIn("ollama pull", result)
        
    def test_500_internal_server_error(self):
        """Test 500 Internal Server Error message"""
        result = get_error_message(500)
        self.assertIn("Error 500", result)
        self.assertIn("Internal Server Error", result)
        self.assertIn("out of memory", result)
        self.assertIn("ollama serve", result)
        
    def test_503_service_unavailable(self):
        """Test 503 Service Unavailable error message"""
        result = get_error_message(503)
        self.assertIn("Error 503", result)
        self.assertIn("Service Unavailable", result)
        self.assertIn("ollama serve", result)
        self.assertIn("port 11434", result)
        
    def test_unknown_status_code(self):
        """Test handling of unknown/unmapped status codes"""
        result = get_error_message(418)  # I'm a teapot
        self.assertIn("Error 418", result)
        self.assertIn("Request failed", result)
        self.assertIn("documentation", result)
        
    def test_all_known_codes_have_suggestions(self):
        """Verify all known error codes include suggestions"""
        known_codes = [400, 403, 404, 500, 503]
        for code in known_codes:
            result = get_error_message(code)
            self.assertIn("Suggestions", result, 
                         f"Status code {code} should include suggestions")
            
    def test_error_messages_are_strings(self):
        """Verify all error messages return strings"""
        test_codes = [400, 403, 404, 500, 503, 999]
        for code in test_codes:
            result = get_error_message(code)
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)


class TestErrorMessageQuality(unittest.TestCase):
    """Test the quality and completeness of error messages"""
    
    def test_messages_contain_actionable_advice(self):
        """Verify error messages have actionable troubleshooting steps"""
        actionable_keywords = ['check', 'verify', 'try', 'ensure', 'install']
        
        for code in [400, 403, 404, 500, 503]:
            result = get_error_message(code).lower()
            has_actionable = any(keyword in result for keyword in actionable_keywords)
            self.assertTrue(has_actionable, 
                          f"Error {code} should have actionable advice")
            
    def test_messages_mention_ollama_command(self):
        """Verify relevant messages mention ollama commands"""
        ollama_command_codes = [404, 500, 503]
        
        for code in ollama_command_codes:
            result = get_error_message(code).lower()
            self.assertIn('ollama', result, 
                         f"Error {code} should mention ollama commands")
            
    def test_error_messages_are_readable(self):
        """Verify error messages are formatted for readability"""
        for code in [400, 403, 404, 500, 503]:
            result = get_error_message(code)
            # Should have multiple lines for readability
            self.assertGreater(result.count('\n'), 2, 
                             f"Error {code} should be multi-line")


class TestGenerateMessageIntegration(unittest.TestCase):
    """Integration tests for generate_message with error handling
    
    Note: These tests are optional and will be skipped if commands.py 
    cannot be imported (e.g., if dependencies are missing).
    """
    
    @classmethod
    def setUpClass(cls):
        """Try to import commands module, skip tests if unavailable"""
        cls.commands_available = False
        try:
            # Mock dependencies before importing commands
            sys.modules['commizard.git_utils'] = MagicMock()
            sys.modules['commizard.llm_providers'] = MagicMock()
            sys.modules['commizard.output'] = MagicMock()
            
            # Try importing commands
            from commands import generate_message
            cls.commands_available = True
            cls.generate_message = generate_message
        except ImportError as e:
            print(f"\nSkipping integration tests: {e}")
    
    def setUp(self):
        """Skip all tests in this class if commands not available"""
        if not self.__class__.commands_available:
            self.skipTest("commands module not available")
    
    @patch('commizard.git_utils.get_clean_diff')
    @patch('commizard.llm_providers.generate')
    @patch('commizard.output.print_warning')
    def test_no_changes_warning(self, mock_warning, mock_generate, mock_diff):
        """Test handling when there are no git changes"""
        mock_diff.return_value = ""
        
        self.__class__.generate_message([])
        
        mock_warning.assert_called_once_with("No changes to the repository.")
        mock_generate.assert_not_called()
        
    @patch('commizard.git_utils.get_clean_diff')
    @patch('commizard.llm_providers.generate')
    @patch('commizard.llm_providers.generation_prompt', 'Generate commit: ')
    @patch('commizard.output.print_error')
    def test_http_error_handling(self, mock_error, mock_generate, mock_diff):
        """Test HTTP error codes are handled with friendly messages"""
        mock_diff.return_value = "some diff content"
        mock_generate.return_value = (404, "Not found")
        
        self.__class__.generate_message([])
        
        # Verify error handler was called
        mock_error.assert_called_once()
        error_msg = mock_error.call_args[0][0]
        
        # Check the error message is from our handler
        self.assertIn("Error 404", error_msg)
        self.assertIn("Model Not Found", error_msg)
        self.assertIn("ollama pull", error_msg)
        
    @patch('commizard.git_utils.get_clean_diff')
    @patch('commizard.llm_providers.generate')
    @patch('commizard.output.print_error')
    def test_connection_error_handling(self, mock_error, mock_generate, mock_diff):
        """Test non-HTTP errors are passed through directly"""
        mock_diff.return_value = "some diff content"
        mock_generate.return_value = (1, "Connection refused")
        
        self.__class__.generate_message([])
        
        # Should print the raw error message for non-HTTP errors
        mock_error.assert_called_once_with("Connection refused")
        
    @patch('commizard.git_utils.get_clean_diff')
    @patch('commizard.llm_providers.generate')
    @patch('commizard.llm_providers.generation_prompt', 'Generate commit: ')
    @patch('commizard.output.print_generated')
    @patch('commizard.output.wrap_text')
    def test_successful_generation(self, mock_wrap, mock_print_gen, 
                                   mock_generate, mock_diff):
        """Test successful message generation"""
        mock_diff.return_value = "some diff content"
        mock_generate.return_value = (0, "feat: add new feature")
        mock_wrap.return_value = "feat: add new feature"
        
        self.__class__.generate_message([])
        
        mock_print_gen.assert_called_once_with("feat: add new feature")


def run_manual_tests():
    """Manual testing function to see actual output"""
    print("=" * 70)
    print("MANUAL ERROR MESSAGE TESTING")
    print("=" * 70)
    print()
    
    test_codes = [400, 403, 404, 500, 503, 418]
    
    for code in test_codes:
        print(f"\n{'=' * 70}")
        print(f"Testing Status Code: {code}")
        print('=' * 70)
        print(get_error_message(code))
        print()


def main():
    """Main test runner"""
    print("=" * 70)
    print("OLLAMA ERROR HANDLER TEST SUITE")
    print("=" * 70)
    print()
    
    # Run unit tests
    print("Running unit tests...\n")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaErrors))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorMessageQuality))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerateMessageIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Show manual tests
    print("\n" * 2)
    run_manual_tests()
    
    # Print summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#generated using LLM