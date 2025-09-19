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
            assert f"]{char}" in result
