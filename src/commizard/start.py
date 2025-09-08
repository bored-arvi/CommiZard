import shutil

from rich.color import Color
from rich.console import Console

text_banner = r"""
 ██████╗ ██████╗ ███╗   ███╗███╗   ███╗██╗███████╗ █████╗ ██████╗ ██████╗
██╔════╝██╔═══██╗████╗ ████║████╗ ████║██║╚══███╔╝██╔══██╗██╔══██╗██╔══██╗
██║     ██║   ██║██╔████╔██║██╔████╔██║██║  ███╔╝ ███████║██████╔╝██║  ██║
██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║███████╗██║  ██║██║  ██║██████╔╝
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
"""

# Gradient colors
start_color = Color.parse("#535147")
start_color = Color.parse("#FF746C")
end_color = Color.parse("#8F00FF")


def gradient_text(text: str, start_color: Color, end_color: Color) -> str:
    """
    Apply a horizontal gradient across the given ASCII art text.

    Args:
        text: The ASCII art or banner text.
        start_color: The starting Rich color object.
        end_color: The ending Rich color object.

    Returns:
        str: The ASCII text wrapped in Rich markup with gradient colors.
    """
    lines = text.splitlines()
    total_chars = max(len(line) for line in lines)
    result_lines = []
    for line in lines:
        colored_line = ""
        for i, char in enumerate(line):
            r = int(start_color.triplet[0] + (
                    end_color.triplet[0] - start_color.triplet[0]) * (
                            i / total_chars))
            g = int(
                start_color.triplet[1] + (
                        end_color.triplet[1] - start_color.triplet[1]) * (
                        i / total_chars))
            b = int(start_color.triplet[2] + (
                    end_color.triplet[2] - start_color.triplet[2]) * (
                            i / total_chars))
            colored_line += f"[#{r:02x}{g:02x}{b:02x}]{char}"
        result_lines.append(colored_line)
    return "\n".join(result_lines)


# TODO: randomly chooses the colors so the welcome screen is different
#       everytime the program is run.
def print_welcome() -> None:
    """
    Print the welcome screen. Right now it's the ASCII art of the project's
    name.

    Returns:
        None
    """
    console = Console()
    if console.color_system == "truecolor":
        console.print(gradient_text(text_banner, start_color, end_color))

    # don't use the gradient function for terminals that don't support it:
    else:
        console.print(f"[bold purple]{text_banner}[/bold purple]")


def check_git_installed() -> bool:
    """
    Check if the git package is installed.

    Returns:
        bool: True if the package is installed, False otherwise.
    """
    return shutil.which("git") != None


def check_local_ai() -> bool:
    """
    Check if there's an ollama server running on port 11434

    Returns:
        True if there's a local AI server running, False otherwise.
    """
