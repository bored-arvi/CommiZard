import unittest
from unittest.mock import patch, MagicMock
from commizard.commands import generate_message


class TestGenerateMessage(unittest.TestCase):
    """
    Robust test suite for `generate_message()` with explicit checks
    for each distinct code path: warnings, HTTP errors, connection issues,
    and successful generation.
    """

    # ----------------------------------------------------------------------
    # Test Case 1: No Git Changes (Warning Expected)
    # ----------------------------------------------------------------------
    @patch("commizard.output.print_warning")
    @patch("commizard.git_utils.get_clean_diff", return_value="")
    def test_no_changes_triggers_warning(self, mock_diff, mock_warning):
        """If the repository has no changes, it should warn and stop."""
        generate_message([])
        mock_warning.assert_called_once_with("No changes to the repository.")
        # Verify no further operations occur
        mock_diff.assert_called_once()

    # ----------------------------------------------------------------------
    # Test Case 2: HTTP Error Handling (e.g., 404)
    # ----------------------------------------------------------------------
    @patch("commizard.output.print_error")
    @patch("commizard.llm_providers.generate", return_value=(404, "Model Not Found"))
    @patch("commizard.git_utils.get_clean_diff", return_value="some diff")
    def test_http_error_code_produces_friendly_message(self, mock_diff, mock_generate, mock_error):
        """If Ollama returns an HTTP-like status code, a friendly error message should be printed."""
        generate_message([])
        mock_generate.assert_called_once()
        mock_error.assert_called_once()
        error_msg = mock_error.call_args[0][0]
        self.assertIn("Error 404", error_msg)
        self.assertIn("Model Not Found", error_msg)

    # ----------------------------------------------------------------------
    # Test Case 3: Connection Error (Non-HTTP)
    # ----------------------------------------------------------------------
    @patch("commizard.output.print_error")
    @patch("commizard.llm_providers.generate", side_effect=ConnectionRefusedError)
    @patch("commizard.git_utils.get_clean_diff", return_value="some diff")
    def test_connection_refused_handling(self, mock_diff, mock_generate, mock_error):
        """If the LLM provider cannot connect, the function should display 'Connection refused'."""
        generate_message([])
        mock_generate.assert_called_once()
        mock_error.assert_called_once_with("Connection refused")

    # ----------------------------------------------------------------------
    # Test Case 4: Non-HTTP Custom Error (e.g., status=1)
    # ----------------------------------------------------------------------
    @patch("commizard.output.print_error")
    @patch("commizard.llm_providers.generate", return_value=(1, "Socket timeout"))
    @patch("commizard.git_utils.get_clean_diff", return_value="some diff")
    def test_non_http_error_message_displayed(self, mock_diff, mock_generate, mock_error):
        """If a non-HTTP error occurs (e.g., code=1), the raw error should be shown."""
        generate_message([])
        mock_error.assert_called_once_with("Socket timeout")

    # ----------------------------------------------------------------------
    # Test Case 5: Successful Commit Message Generation
    # ----------------------------------------------------------------------
    @patch("commizard.output.print_generated")
    @patch("commizard.output.wrap_text", side_effect=lambda text, width: text)
    @patch("commizard.llm_providers.generate", return_value=(0, "feat: add login API"))
    @patch("commizard.git_utils.get_clean_diff", return_value="some diff")
    def test_successful_generation_prints_result(self, mock_diff, mock_generate, mock_wrap, mock_print_gen):
        """When generation succeeds, the commit message should be wrapped and printed."""
        generate_message([])

        # Ensure the correct message was processed and printed
        mock_wrap.assert_called_once_with("feat: add login API", 72)
        mock_print_gen.assert_called_once_with("feat: add login API")

    # ----------------------------------------------------------------------
    # Test Case 6: Unexpected Exception (safety net)
    # ----------------------------------------------------------------------
    @patch("commizard.output.print_error")
    @patch("commizard.git_utils.get_clean_diff", side_effect=RuntimeError("unexpected"))
    def test_unexpected_exception_is_caught(self, mock_diff, mock_error):
        """Any unhandled exception should be caught and displayed cleanly."""
        generate_message([])
        mock_error.assert_called_once()
        err_msg = mock_error.call_args[0][0]
        self.assertIn("Unexpected error:", err_msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
