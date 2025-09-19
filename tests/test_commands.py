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

    # mock the behavior of mock_init
    mock_init.side_effect = lambda x: monkeypatch.setattr(llm_providers,
                                                          "available_models",
                                                          ["grok", "GPT"])
    commands.start_model(opts)

    if expect_init:
        mock_init.assert_called_once()
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


@pytest.mark.parametrize(
    "available_models, opts",
    [
        ([], "-v"),
        (["gpt-1"], "-q"),
        (["gpt-1", "gpt-2", "gpt-3"], "--all-info"),
    ]
)
@patch("builtins.print")  # thanks chat-GPT. I never would've found this.
@patch("commizard.llm_providers.init_model_list")
def test_print_available_models(mock_init, mock_print, available_models, opts,
                                monkeypatch):
    mock_init.side_effect = lambda: setattr(llm_providers, "available_models",
                                            available_models)
    commands.print_available_models(opts)

    mock_init.assert_called_once()

    # assert prints match number of models
    assert mock_print.call_count == len(available_models)

    for model in available_models:
        mock_print.assert_any_call(model)


@pytest.mark.parametrize(
    "opts",
    [
        [],  # no options
        ["--dry-run"],  # single option
        ["--foo", "--bar"],  # multiple options
    ]
)
@patch("commizard.llm_providers.generate")
def test_generate_message(mock_generate, opts):
    commands.generate_message(opts)

    mock_generate.assert_called_once_with()
