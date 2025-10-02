import os, platform, shutil, sys

def clear_screen() -> None:
    """
    Clear the terminal on Windows/macOS/Linux.
    """
    if platform.system().lower().startswith("win"):
        cmd = "cls"
    else:
        cmd = "clear"

    if shutil.which(cmd):
        os.system(cmd)
        return

    # fallback: ANSI escape
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
