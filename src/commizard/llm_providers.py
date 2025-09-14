import requests

from . import output

available_models = None
selected_model = None

gen_head = ""
gen_body = ""

generation_prompt = """You are an assistant that writes Git commit messages.

Write a commit message based on the following git diff:
- Provide a short, descriptive commit title in imperative mood (e.g., "fix parser bug").
- Keep the title under 50 characters if possible.
- If relevant, also include a body with more details.
- Do not include anything except the commit message.

Here is the diff:
"""


def init_model_list() -> None:
    """
    Initialize the list of available models inside the available_models global
    variable.
    """
    global available_models
    available_models = list_locals()


def list_locals() -> list[str]:
    """
    return a list of available local AI models
    """
    # TODO: Handle potential errors
    response = requests.get('http://localhost:11434/api/tags', timeout=0.3)

    # Right now we assume that the response is OK:
    response = response.json()
    response = response["models"]
    output = []

    # TODO: also return the number of parameters to display a better list
    for model in response:
        output.append(model["name"])

    return output


def select_model(select_str: str) -> None:
    """
    Prepare the local model for use
    """
    global selected_model
    selected_model = select_str
    load_res = load_model(selected_model)
    if load_res.get("done_reason") == "load":
        output.print_success(f"{selected_model} loaded.")


def load_model(model_name: str) -> dict:
    """
    Load the local model into RAM
    Args:
        model_name: name of the model to load

    Returns:
        a dict of the POST request
    """
    print("Loading local model...")
    payload = {"model": selected_model}
    try:
        r = requests.post("http://localhost:11434/api/generate", json=payload)
    except requests.exceptions.ConnectionError:
        output.print_error(
            f"Failed to connect to {model_name}. Is ollama running?")
        return {}
    return r.json()


def generate() -> None:
    """
    generate commit message
    """
    pass


def regenerate(prompt: str) -> None:
    """
    regenerate commit message based on prompt
    """
    pass
