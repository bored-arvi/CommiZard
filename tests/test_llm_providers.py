from unittest.mock import patch, Mock

import pytest
import requests

from commizard import llm_providers as llm


@pytest.mark.parametrize(
    "response, return_code, expected_is_error, expected_err_message",
    [
        # Non-error responses
        ("ok", 200, False, ""),
        ("created", 201, False, ""),
        ("empty", 0, False, ""),
        ({"reason": "not found"}, 404, False, ""),

        # Error cases
        ("404", -1, True, "can't connect to the server"),
        ("success", -2, True, "HTTP error occurred"),
        ({1: "found"}, -3, True, "too many redirects"),
        ("", -4, True, "the request timed out"),
    ],
)
def test_HttpResponse(response, return_code, expected_is_error,
                      expected_err_message):
    http_resp = llm.HttpResponse(response, return_code)

    assert http_resp.response == response
    assert http_resp.return_code == return_code
    assert http_resp.is_error() == expected_is_error
    assert http_resp.err_message() == expected_err_message


@pytest.mark.parametrize(
    "method, return_value, side_effect, expected_response, expected_code,"
    "expected_exception",
    [
        # --- Success cases ---
        ("GET", {"json": {"key": "val"}, "status": 200}, None, {"key": "val"},
         200, None),
        ("GET", {"json": requests.exceptions.JSONDecodeError("err", "doc", 0),
                 "text": "plain text", "status": 200}, None, "plain text", 200,
         None),
        ("POST", {"json": {"ok": True}, "status": 201}, None, {"ok": True}, 201,
         None),
        ("GET", {"json": {"key": "val"}, "status": 503}, None, {"key": "val"},
         503, None),

        # --- Error branches ---
        ("GET", None, requests.ConnectionError, None, -1, None),
        ("GET", None, requests.HTTPError, None, -2, None),
        ("GET", None, requests.TooManyRedirects, None, -3, None),
        ("GET", None, requests.Timeout, None, -4, None),
        ("GET", None, requests.RequestException, None, -5, None),

        # --- Invalid methods ---
        ("PUT", None, None, None, None, NotImplementedError),
        ("FOO", None, None, None, None, ValueError),
    ],
)
@patch("requests.get")
@patch("requests.post")
def test_http_request(mock_post, mock_get, method, return_value, side_effect,
                      expected_response, expected_code, expected_exception):
    # pick which mock to configure
    mock_target = None
    if method.upper() == "GET":
        mock_target = mock_get
    elif method.upper() == "POST":
        mock_target = mock_post

    # setup mock_target based on the return_value dict
    if mock_target:
        if side_effect:
            mock_target.side_effect = side_effect
        else:
            mock_resp = Mock()
            mock_resp.status_code = return_value["status"]
            if isinstance(return_value.get("json"), Exception):
                mock_resp.json.side_effect = return_value["json"]
            else:
                mock_resp.json.return_value = return_value.get("json")
            mock_resp.text = return_value.get("text")
            mock_target.return_value = mock_resp

    if expected_exception:
        with pytest.raises(expected_exception):
            llm.http_request(method, "http://test.com")
    else:
        result = llm.http_request(method, "http://test.com")
        assert isinstance(result, llm.HttpResponse)
        assert result.response == expected_response
        assert result.return_code == expected_code


@patch("commizard.llm_providers.list_locals")
def test_init_model_list(mock_list, monkeypatch):
    monkeypatch.setattr(llm, "available_models", None)
    llm.init_model_list()
    mock_list.assert_called_once()


@pytest.mark.parametrize(
    "load_return, expect_success",
    [
        ({"done_reason": "load"}, True),
        ({"done_reason": "other"}, False),
    ],
)
@patch("commizard.llm_providers.output.print_success")
@patch("commizard.llm_providers.load_model")
def test_select_model(mock_load_model, mock_print_success, monkeypatch,
                      load_return, expect_success):
    monkeypatch.setattr(llm, "selected_model", None)
    mock_load_model.return_value = load_return

    llm.select_model("cool_model")

    assert llm.selected_model == "cool_model"

    mock_load_model.assert_called_once_with("cool_model")

    if expect_success:
        mock_print_success.assert_called_once_with("cool_model loaded.")
    else:
        mock_print_success.assert_not_called()


@pytest.mark.parametrize(
    "is_error, response, expected_result, expect_error",
    [
        # http_request returns error
        (True, None, [], True),
        # http_request succeeds with models
        (False, {"models": [{"name": "model1"}, {"name": "model2"}]},
         ["model1", "model2"], False),
        # http_request succeeds but no models
        (False, {"models": []}, [], False),
    ],
)
@patch("commizard.llm_providers.output.print_error")
@patch("commizard.llm_providers.http_request")
def test_list_locals(mock_http_request, mock_print_error,
                     is_error, response, expected_result, expect_error):
    fake_response = Mock()
    fake_response.is_error.return_value = is_error
    fake_response.response = response
    mock_http_request.return_value = fake_response

    result = llm.list_locals()
    assert result == expected_result
    if expect_error:
        mock_print_error.assert_called_once_with(
            "failed to list available local AI models. Is ollama running?")
    else:
        mock_print_error.assert_not_called()
    mock_http_request.assert_called_once_with("GET",
                                              "http://localhost:11434/api/tags",
                                              timeout=0.3)


@pytest.mark.parametrize(
    "is_error, response, expect_error, expected_result",
    [
        (True, None, True, {}),
        (False, {"done_reason": "load"}, False, {"done_reason": "load"}),
    ],
)
@patch("commizard.llm_providers.output.print_error")
@patch("commizard.llm_providers.http_request")
def test_load_model(mock_http_request, mock_print_error, monkeypatch, is_error,
                    response, expect_error, expected_result):
    fake_response = Mock()
    fake_response.is_error.return_value = is_error
    fake_response.response = response
    mock_http_request.return_value = fake_response
    monkeypatch.setattr(llm, "selected_model", "patched_model")
    result = llm.load_model("test_model")

    mock_http_request.assert_called_once_with("POST",
                                              "http://localhost:11434/api/generate",
                                              json={"model": "patched_model"})
    if expect_error:
        mock_print_error.assert_called_once_with(
            "Failed to load test_model. Is ollama running?")
    else:
        mock_print_error.assert_not_called()
    assert result == expected_result


@patch("commizard.llm_providers.http_request")
def test_unload_model(mock_http_request, monkeypatch):
    monkeypatch.setattr(llm, "selected_model", "mymodel")
    llm.unload_model()
    mock_http_request.assert_called_once_with(
        "POST", "http://localhost:11434/api/generate", json={"model": "mymodel",
                                                             "keep_alive": 0})
    assert llm.selected_model is None


@pytest.mark.parametrize(
    "diff, expected_gen_message, expect_warning, expect_http",
    [
        ("", None, True, False),
        ("diff --git a/file.txt b/file.txt", "Generated commit message", False,
         True),
    ],
)
@patch("commizard.llm_providers.output.print_generated")
@patch("commizard.llm_providers.output.wrap_text")
@patch("commizard.llm_providers.http_request")
@patch("commizard.llm_providers.git_utils.get_diff")
@patch("commizard.llm_providers.output.print_warning")
def test_generate(mock_print_warning, mock_get_diff, mock_http_request,
                  mock_wrap_text, mock_print_generated, monkeypatch,
                  diff, expected_gen_message, expect_warning, expect_http):
    monkeypatch.setattr(llm, "selected_model", "my_model")
    monkeypatch.setattr(llm, "gen_message", None)

    mock_get_diff.return_value = diff
    mock_wrap_text.return_value = expected_gen_message
    # Configure http_request / wrap_text if HTTP is expected
    if expect_http:
        fake_response = Mock()
        fake_response.response = {"response": " the sky is black, I'm dumb\n"}
        mock_http_request.return_value = fake_response

    llm.generate()

    # Assert warning
    if expect_warning:
        mock_print_warning.assert_called_once_with(
            "No changes to the repository.")
    else:
        mock_print_warning.assert_not_called()

    if expect_http:
        mock_http_request.assert_called_once_with(
            "POST", "http://localhost:11434/api/generate",
            json={"model": "my_model",
                  "prompt": llm.generation_prompt + diff,
                  "stream": False
                  }
        )
        mock_wrap_text.assert_called_once()
        mock_print_generated.assert_called_once_with(expected_gen_message)
        assert llm.gen_message == expected_gen_message
    else:
        mock_http_request.assert_not_called()
        assert llm.gen_message is None


@pytest.mark.parametrize(
    "select_str, load_val, should_print",
    [
        ("modelA", {"done_reason": "load"}, True),
        ("modelB", {"done_reason": "error"}, False),
        ("modelC", {}, False),
    ]
)
@patch("commizard.llm_providers.load_model")
@patch("commizard.llm_providers.output.print_success")
def test_select_model(mock_print, mock_load, select_str, load_val,
                      should_print, monkeypatch):
    monkeypatch.setattr(llm, "selected_model", None)

    mock_load.return_value = load_val

    llm.select_model(select_str)
    assert llm.selected_model == select_str
    mock_load.assert_called_once_with(select_str)

    if should_print:
        mock_print.assert_called_once_with(f"{llm.selected_model} loaded.")
    else:
        mock_print.assert_not_called()
