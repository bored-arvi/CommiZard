from . import commands
from . import start
from .output import *


# TODO: add a printing handler to print colorized outputs to the terminal
#       (errors, results, warnings, verbose diagnostics, etc.)

# TODO: Consider multithreading startup checks. If you're using timeouts and
#       long waits, the program will halt executing and not be responsive enough
def main() -> None:
    """
    Main function of the program.

    Returns:
        None
    """
    if not start.check_git_installed():
        print_error("git not installed")
        return

    if not start.local_ai_available():
        print_warning("local AI not available")

    if not start.is_inside_working_tree():
        print_error("not inside work tree")

    start.print_welcome()

    while True:
        user_input = input("CommiZard> ").strip()
        if user_input in ("exit", "quit"):
            print("Goodbye!")
            break
        commands.parser(user_input)


if __name__ == "__main__":
    main()
