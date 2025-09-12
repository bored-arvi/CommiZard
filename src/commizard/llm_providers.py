import requests

available_models = []
selected_model = ""

gen_head = ""
gen_body = ""


def list_locals() -> list[str]:
    """
    return a list of available local AI models
    """
    response = requests.get('http://localhost:11434/api/tags', timeout=1)
    ...


available_models += list_locals()


def select_model(select_str: str) -> None:
    """
    change selected_model to select_str if available
    """
    if select_str in available_models:
        selected_model = select_str
        # TODO: Load the model
        ...


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
