import shutil

import pytest
from commizard import start
from rich.color import Color


@pytest.mark.parametrize(
    "text, start_color, end_color, expected_substrings",
    [
        (
                "Hi",
                Color.from_rgb(255, 0, 0),  # red
                Color.from_rgb(0, 0, 255),  # blue
                ["[#ff0000]H", "[#7f007f]i"],
        ),
        (
                "OK",
                Color.from_rgb(0, 255, 0),  # green
                Color.from_rgb(0, 255, 0),  # same color
                ["[#00ff00]O", "[#00ff00]K"],
        ),
        (
                "X",
                Color.from_rgb(0, 0, 0),  # black
                Color.from_rgb(255, 255, 255),  # white
                ["[#000000]X"],
        ),
        (
                "Yo\nHi",
                Color.from_rgb(0, 0, 255),  # blue
                Color.from_rgb(255, 0, 0),  # red
                ["[#0000ff]Y", "[#7f007f]o", "[#0000ff]H", "[#7f007f]i"],
                # checks gradient + newline preserved
        ),
        # Case 6: Longer string gradient black → white
        (
                "ABCDE",
                Color.from_rgb(0, 0, 0),  # black
                Color.from_rgb(255, 255, 255),  # white
                ["[#000000]A", "[#333333]B", "[#666666]C", "[#999999]D",
                 "[#cccccc]E"],
        ),
    ],
)
def test_gradient_text(text, start_color, end_color, expected_substrings):
    result = start.gradient_text(text, start_color, end_color)

    # Ensure all expected substrings appear in the result
    for substring in expected_substrings:
        assert substring in result

    # Check result structure: every char should be wrapped
    for char in text:
        if char != "\n":
            assert "[#" in result
            assert f"]{char}" in result


@pytest.mark.parametrize("color_system, expect_gradient", [
    ("truecolor", True),
    ("256", True),
    ("windows", False),
    (None, False),
])
def test_print_welcome(monkeypatch, capsys, color_system, expect_gradient):
    # class to patch instead of rich.Console() class
    class DummyConsole:
        def __init__(self):
            self.color_system = color_system

        def print(self, msg):
            print(msg)

    monkeypatch.setattr(start, "Console", DummyConsole)

    start.print_welcome()

    # Hook to stdout
    captured = capsys.readouterr().out

    if expect_gradient:
        assert "[#" in captured
    else:
        # Should contain fallback purple markup
        assert "[bold purple]" in captured


@pytest.mark.parametrize("git_path, expected", [
    ("/usr/bin/git", True),
    ("C:\\Program Files\\Git\\cmd\\git.EXE", True),
    (None, False),
    ("some/other/path/maybe/in/macOS", True),
])
def test_check_git_installed(monkeypatch, git_path, expected):
    # Monkeypatch shutil.which to simulate environment
    monkeypatch.setattr(shutil, "which",
                        lambda cmd: git_path if cmd == "git" else None)

    assert start.check_git_installed() is expected
