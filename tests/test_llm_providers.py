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
def test_http_response(response, return_code, expected_is_error,
                       expected_err_message):
    http_resp = llm.HttpResponse(response, return_code)

    assert http_resp.response == response
    assert http_resp.return_code == return_code
    assert http_resp.is_error() == expected_is_error
    assert http_resp.err_message() == expected_err_message


@pytest.mark.parametrize(
    "method, url, target, side_effect, json_value, text_value, status_code,"
    "expected_response, expected_code, expected_exception",
    [
        # --- Success cases ---
        # GET with JSON
        ("GET", "http://test.com", "requests.get", None, {"key": "val"}, None,
         200, {"key": "val"}, 200, None),

        # GET with text (json raises JSONDecodeError)
        ("GET", "http://test.com", "requests.get", None,
         requests.exceptions.JSONDecodeError("err", "doc", 0),
         "plain text", 200, "plain text", 200, None),

        # POST with JSON
        ("POST", "http://test.com", "requests.post", None, {"ok": True}, None,
         201, {"ok": True}, 201, None),

        # --- Error branches ---
        ("GET", "http://test.com", "requests.get", requests.ConnectionError,
         None, None, None, None, -1, None),
        ("GET", "http://test.com", "requests.get", requests.HTTPError, None,
         None, None, None, -2, None),
        ("GET", "http://test.com", "requests.get", requests.TooManyRedirects,
         None, None, None, None, -3, None),
        ("GET", "http://test.com", "requests.get", requests.Timeout, None, None,
         None, None, -4, None),
        ("GET", "http://test.com", "requests.get", requests.RequestException,
         None, None, None, None, -5, None),

        # --- Invalid methods ---
        ("PUT", "http://test.com", None, None, None, None, None, None, None,
         NotImplementedError),
        ("FOO", "http://test.com", None, None, None, None, None, None, None,
         ValueError),
    ],
)
@patch("requests.get")
@patch("requests.post")
def test_http_request(
        mock_post, mock_get,
        method, url, target, side_effect, json_value, text_value, status_code,
        expected_response, expected_code, expected_exception
):
    # select which mock to configure, if any
    mock_target = None
    if target:
        mock_target = mock_get if target.endswith("get") else mock_post

    if mock_target:
        if side_effect:
            mock_target.side_effect = side_effect
        else:
            mock_resp = Mock()
            mock_resp.status_code = status_code
            if isinstance(json_value, Exception):
                mock_resp.json.side_effect = json_value
            else:
                mock_resp.json.return_value = json_value
            mock_resp.text = text_value
            mock_target.return_value = mock_resp

    if expected_exception:
        with pytest.raises(expected_exception):
            llm.http_request(method, url)
    else:
        result = llm.http_request(method, url)
        assert isinstance(result, llm.HttpResponse)
        assert result.return_code == expected_code
        assert result.response == expected_response


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
