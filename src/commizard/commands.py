from __future__ import annotations

import os
import platform
import sys
from typing import TYPE_CHECKING

import pyperclip

from . import git_utils, llm_providers, output

if TYPE_CHECKING:
    from collections.abc import Callable


def get_error_message(status_code: int) -> str:
    """
    Return user-friendly error message for Ollama HTTP status codes.

    Ollama follows standard REST API conventions with these common responses:
    - 200/201: Success / Can be ignored
    - 400: Bad Request (malformed request)
    - 403: Forbidden (access denied, check OLLAMA_ORIGINS)
    - 404: Not Found (model doesn't exist)
    - 500: Internal Server Error (model crashed or out of memory)
    - 503: Service Unavailable (Ollama not running)

    Args:
        status_code: HTTP status code from Ollama API

    Returns:
        User-friendly error message with troubleshooting suggestions
    """
    error_messages = {
        400: (
            "Bad Request - The request was malformed or contains invalid parameters.\n"
            "Suggestions:\n"
            "  • Check if your prompt is properly formatted\n"
            "  • Verify all required parameters are provided\n"
            "  • Ensure the model name is correct"
        ),
        403: (
            "Forbidden - Access to Ollama was denied.\n"
            "Suggestions:\n"
            "  • Check OLLAMA_ORIGINS environment variable\n"
            "  • Verify Ollama accepts requests from your application\n"
            "  • Ensure proper permissions to access the service"
        ),
        404: (
            "Model Not Found - The requested model doesn't exist.\n"
            "Suggestions:\n"
            "  • Install the model: ollama pull <model-name>\n"
            "  • Check available models with the 'list' command\n"
            "  • Verify the model name spelling"
        ),
        500: (
            "Internal Server Error - Ollama encountered an unexpected error.\n"
            "Suggestions:\n"
            "  • The model may have run out of memory (RAM/VRAM)\n"
            "  • Try restarting Ollama: ollama serve\n"
            "  • Check Ollama logs for detailed error information\n"
            "  • Consider using a smaller model if resources are limited"
        ),
        503: (
            "Service Unavailable - Ollama service is not responding.\n"
            "Suggestions:\n"
            "  • Start Ollama: ollama serve\n"
            "  • Check if Ollama is running: ps aux | grep ollama\n"
            "  • Verify the service is listening on port 11434\n"
            "  • Wait a moment if the service is starting up"
        ),
    }

    if status_code in error_messages:
        return f"Error {status_code}: {error_messages[status_code]}"

    # Generic fallback for unknown status codes
    return (
        f"Error {status_code}: Request failed.\n"
        "Check the Ollama documentation or server logs for more details."
    )


def handle_commit_req(opts: list[str]) -> None:
    """
    commits the generated prompt. prints an error message if commiting fails
    """
    if llm_providers.gen_message is None or llm_providers.gen_message == "":
        output.print_warning("No commit message detected. Skipping.")
        return
    out, msg = git_utils.commit(llm_providers.gen_message)
    if out == 0:
        output.print_success(msg)
    else:
        output.print_warning(msg)


# TODO: implement
def print_help(opts: list[str]) -> None:
    """
    prints a list of all commands and a brief description

    Args:
        opts: a specific command that the user needs help with

    Returns:
        None
    """


def copy_command(opts: list[str]) -> None:
    """
    copies the generated prompt to clipboard according to options passed.

    Args:
        opts: list of options following the command
    """
    if llm_providers.gen_message is None:
        output.print_warning(
            "No generated message found. Please run 'generate' first."
        )
        return

    pyperclip.copy(llm_providers.gen_message)
    output.print_success("Copied to clipboard.")


def start_model(opts: list[str]) -> None:
    """
    Get the model (either local or online) ready for generation based on the
    options passed.
    """
    if llm_providers.available_models is None:
        llm_providers.init_model_list()

    if opts == []:
        output.print_error("Please specify a model.")
        return

    # TODO: see issue #42
    model_name = opts[0]

    if (
        llm_providers.available_models
        and model_name not in llm_providers.available_models
    ):
        output.print_error(f"{model_name} Not found.")
        return
    llm_providers.select_model(model_name)


def print_available_models(opts: list[str]) -> None:
    """
    prints the available models according to options passed.
    """
    llm_providers.init_model_list()
    if llm_providers.available_models is None:
        output.print_error(
            "failed to list available local AI models. Is ollama running?"
        )
        return
    elif not llm_providers.available_models:
        output.print_warning("No local AI models found.")
        return
    for model in llm_providers.available_models:
        print(model)


def generate_message(opts: list[str]) -> None:
    """
    Generate a commit message using Ollama with improved error handling.
    """
    try:
        diff = git_utils.get_clean_diff()
        if not diff:
            output.print_warning("No changes to the repository.")
            return

        prompt = llm_providers.generation_prompt + diff
        stat, res = llm_providers.generate(prompt)

        if stat != 0:
            if 400 <= stat <= 599:
                error_msg = get_error_message(stat)
                output.print_error(error_msg)
            else:
                output.print_error(str(res))
            return

        wrapped_res = output.wrap_text(res, 72)
        llm_providers.gen_message = wrapped_res
        output.print_generated(wrapped_res)

    except ConnectionRefusedError:
        output.print_error("Connection refused")
    except (RuntimeError, ValueError, TypeError) as e:
        # Catch only expected runtime errors
        output.print_error(f"Unexpected error: {e}")


def cmd_clear(opts: list[str]) -> None:
    """
    Clear terminal screen (Windows/macOS/Linux).
    """
    cmd = "cls" if platform.system().lower().startswith("win") else "clear"
    rc = os.system(cmd)  # noqa: S605
    if rc != 0:  # fallback to ANSI if shell command failed
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


supported_commands: dict[str, Callable[[list[str]], None]] = {
    "commit": handle_commit_req,
    "help": print_help,
    "cp": copy_command,
    "start": start_model,
    "list": print_available_models,
    "gen": generate_message,
    "generate": generate_message,
    "clear": cmd_clear,
    "cls": cmd_clear,
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
        cmd_func = supported_commands[commands[0]]
        cmd_func(commands[1:])
        return 0
    else:
        return 1
