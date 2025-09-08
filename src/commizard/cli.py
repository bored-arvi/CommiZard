from . import start


# TODO: add a printing handler to print colorized outputs to the terminal
#       (errors, results, warnings, verbose diagnostics, etc.)

def main() -> None:
    """
    Main function of the program.

    Returns:
        None
    """
    if not start.check_git_installed():
        print("git not installed")
        return

    if not start.local_ai_available():
        print("local ai not available")

    start.print_welcome()
    
    while True:
        command = input("CommiZard> ").strip()
        if command in ("exit", "quit"):
            print("Goodbye!")
            break
        else:
            print(f"You typed: {command}")


if __name__ == "__main__":
    main()
