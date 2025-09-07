from rich.console import Console
from rich.panel import Panel

text_banner = r"""
  ____                              _  _____                _ 
 / ___| ___   _ __ ___   _ __ ___  (_)|__  / __ _  _ __  __| |
| |    / _ \ | '_ ` _ \ | '_ ` _ \ | |  / / / _` || '__|/ _` |
| |___| (_) || | | | | || | | | | || | / /_| (_| || |  | (_| |
 \____|\___/ |_| |_| |_||_| |_| |_||_|/____|\__,_||_|   \__,_|
"""


def print_welcome() -> None:
    console = Console()
    panel = Panel(text_banner, border_style="bright_cyan", expand=False)
    console.print(panel)
