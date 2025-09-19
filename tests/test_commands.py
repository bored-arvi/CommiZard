from unittest.mock import patch

import pytest
from commizard import commands, llm_providers


@pytest.mark.parametrize("gen_message, opts, expect_warning", [
    # No message. warning only
    (None, [], True),
    # copied + success
    ("The sky is blue because of rayleigh scattering", [], False),

])
@patch("pyperclip.copy")
@patch("commizard.output.print_success")
@patch("commizard.output.print_warning")
def test_copy_command(mock_warn, mock_success, mock_copy, gen_message, opts,
                      expect_warning, monkeypatch):
    monkeypatch.setattr(llm_providers, "gen_message", gen_message)
    commands.copy_command(opts)

    if expect_warning:
        mock_warn.assert_called_once()
        mock_success.assert_not_called()
        mock_copy.assert_not_called()
    else:
        mock_warn.assert_not_called()
        mock_success.assert_called_once()
        mock_copy.assert_called_once_with(gen_message)
