import subprocess

from . import output


def handle_commit_req(opts: list) -> int:
    """
    commits the generated prompt according to options:
        If none specified, commits both the Title and the Body
        If passed body or title like : commit body, or: commit title,
        only commits the parts specified.

    Args:
        opts: a list of options following the commit command passed to the cli.

    Returns:
        a status code: 0 for success, 1 for failure, 2 for incorrect
        prompt input.
    """
    if opts == []:
        out = subprocess.run(
            ["git", "commit", "-a", "-m", gen_head, "-m", gen_body],
            capture_output=True)
    elif opts[0] in ("-h", "--help"):
        # TODO: Do something for the helps. This will get super bad super quick
        print("""options:\n
        The commit command will commit both the title and the body by default.\n
        head | title: Just commit the head, ignore the body.\n
        body: Commit the body without the head""")
    elif opts[0] in ("head", "title"):
        out = subprocess.run(
            ["git", "commit", "-a", "-m", gen_head], capture_output=True)
    elif opts[0] == "body":
        out = subprocess.run(
            ["git", "commit", "-a", "-m", gen_body], capture_output=True)
    else:
        output.print_error(f"Error: {opts[0]} is not a valid commit command.")
        return 2


# TODO: implement
def print_help(opts: list) -> None:
    """
    prints a list of all commands and a brief description

    Args:
        opts: a specific command that the user needs help with

    Returns:
        None
    """
    pass


# TODO: implement
def copy_command(opts: list) -> int:
    """
    copies the generated prompt to clipboard according to options passed.

    Args:
        opts: list of options following the command

    Returns:
        a status code: 0 for success, 1 for failure.
    """
    pass


# TODO: implement
def load_model(opts: list) -> int:
    """
    Get the model (either local or online) ready for generation.
    Args:
        opts: list of options following the command

    Returns:
        a status code: 0 for success, 1 for failure.
    """
    pass


supported_commands = {"commit": handle_commit_req,
                      "help": print_help,
                      "cp": copy_command,
                      "start": load_model
                      }


def parser(user_input: str) -> int:
    """
    Parse the user input and call appropriate functions

    Args:
        user_input: The user input to be parsed

    Returns:
        a status code: 0 for success, 1 for unrecognized command
    """
    commands = user_input.split()
    if commands[0] in list(supported_commands.keys()):
        # call the function from the dictionary with the rest of the commands
        # passed as arguments to it
        supported_commands[commands[0]](commands[1:])
        return 0
    else:
        return 1
