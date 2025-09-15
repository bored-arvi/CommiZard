import textwrap

from rich.console import Console

console = Console()


def print_success(message: str) -> None:
    """
    prints success message in green color
    """
    console.print(f"[green]{message}[/green]")


def print_error(message: str) -> None:
    """
    prints error message bold red
    """
    console.print(f"[bold red]Error: {message}[/bold red]")


def print_warning(message: str) -> None:
    """
    prints warning message in yellow color
    """
    console.print(f"[yellow]Warning: {message}[/yellow]")


def print_generated(message: str) -> None:
    """
    prints generated message in blue color
    """
    console.print(f"[blue]{message}[/blue]")


# TODO: add wrapping function for output
def wrap_text(text: str, width: int) -> str:
    """
    Wrap a string to a specified maximum line width by inserting line breaks.
    """
    if width <= 0:
        raise ValueError("Width must be a positive integer")
    return '\n'.join(textwrap.wrap(text, width=width))
