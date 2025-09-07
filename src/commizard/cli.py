from . import start


def main() -> None:
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
