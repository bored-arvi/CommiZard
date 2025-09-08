from rich.console import Console

console = Console()


def print_success(message: str) -> None:
    """
    prints success message in green color

    Args:
        message: success message to print

    Returns:
        None
    """
    console.print(f"[green]{message}[/green]")


def print_error(message: str) -> None:
    """
    prints error message in red color

    Args:
        message: error message to print

    Returns:
        None
    """
    console.print(f"[bold red]Error: {message}[/bold red]")


def print_warning(message: str) -> None:
    """
    prints warning message in yellow color

    Args:
        message: warning message to print

    Returns:
        None
    """
    console.print(f"[yellow]Warning: {message}[/yellow]")


def print_generated(message: str) -> None:
    """
    prints generated message in blue color

    Args:
        message: generated message to print

    Returns:
        None
    """
    console.print(f"[blue]{message}[/blue]")

# TODO: add wrapping function for output
