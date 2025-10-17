import concurrent.futures
import sys
import time

from . import __version__ as version
from . import commands, output, start

help_msg = """
Commit writing wizard

Usage:
  commizard [-v | --version] [-h | --help]

Options:
  -h, --help       Show help for commizard
  -v, --version    Show version information
"""


def handle_args():
    if len(sys.argv) < 2:
        return
    if sys.argv[1] in ("-v", "--version"):
        print(f"CommiZard {version}")
        sys.exit(0)
    elif sys.argv[1] in ("-h", "--help"):
        print(help_msg.strip(), end="\n")
        sys.exit(0)


# TODO: see issue #3
def main() -> None:
    """
    This is the entry point of the program. calls some functions at the start,
    then jumps into an infinite loop.
    """
    strt = time.perf_counter()
    handle_args()
    with concurrent.futures.ThreadPoolExecutor() as exec:
        fut_git = exec.submit(start.check_git_installed)
        fut_ai = exec.submit(start.local_ai_available)
        fut_worktree = exec.submit(start.is_inside_working_tree)
        git_ok = fut_git.result()
        ai_ok = fut_ai.result()
        worktree_ok = fut_worktree.result()

    if not git_ok:
        output.print_error("git not installed")
        return

    if not ai_ok:
        output.print_warning("local AI not available")

    if not worktree_ok:
        output.print_error("not inside work tree")
        return

    start.print_welcome()
    stp = time.perf_counter()
    print(f"took: {round(stp - strt, 3)}")
    while True:
        user_input = input("CommiZard> ").strip()
        if user_input in ("exit", "quit"):
            print("Goodbye!")
            break
        elif user_input == "":
            continue
        commands.parser(user_input)


if __name__ == "__main__":
    main()
