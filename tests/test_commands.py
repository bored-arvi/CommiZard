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


@pytest.mark.parametrize(
    "available_models, opts, expect_init, expect_error, expect_select",
    [
        # init_model_list called
        (None, ["gpt-test"], True, False, False),
        # print_error called
        (["gpt-1", "gpt-2"], ["gpt-3"], False, True, False),
        # select_model called
        (["gpt-1", "gpt-2"], ["gpt-2"], False, False, True),
        # incorrect user input
        (None, [], False, True, False),
        (["gpt-1", "gpt-2"], [], False, True, False),
    ]
)
@patch("commizard.output.print_error")
@patch("commizard.llm_providers.select_model")
@patch("commizard.llm_providers.init_model_list")
def test_start_model(mock_init, mock_select, mock_error, monkeypatch,
                     available_models, opts, expect_init, expect_error,
                     expect_select):
    # set available_models dynamically
    monkeypatch.setattr(llm_providers, "available_models", available_models)

    commands.start_model(opts)

    if expect_init:
        mock_init.assert_called_once()
        # now we mock the behavior of mock_init (setting up available models to
        # now not be None
        monkeypatch.setattr(llm_providers, "available_models", ["grok", "GPT"])
    else:
        mock_init.assert_not_called()

    if expect_error:
        mock_error.assert_called_once_with(f"{opts[0]} Not found.")
    else:
        mock_error.assert_not_called()

    if expect_select:
        mock_select.assert_called_once_with(opts[0])
    else:
        mock_select.assert_not_called()
