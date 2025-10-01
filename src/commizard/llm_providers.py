import requests

from . import git_utils
from . import output

available_models = None
selected_model = None
gen_message = None

# Ironically enough, I've used Chat-GPT to write a prompt to prompt other
# Models (or even itself in the future!)
generation_prompt = """
You are an assistant that generates good, professional Git commit messages.

Guidelines:
- Write a concise, descriptive commit title in **imperative mood** (e.g., "fix
parser bug").
- Keep the title under 50 characters if possible.
- If needed, add a commit body separated by a blank line:
  - Explain *what* changed and *why* (not how).
- Do not include anything except the commit message itself (no commentary or
formatting).
- Do not include Markdown formatting, code blocks, quotes, or symbols such as
``` or **.

Here is the diff:
"""


class HttpResponse:

    def __init__(self, response, return_code):
        self.response = response
        # if the value is less than zero, there's something wrong.
        self.return_code = return_code

    def is_error(self) -> bool:
        return self.return_code < 0

    def err_message(self) -> str:
        if not self.is_error():
            return ""
        err_dict = {
            -1: "can't connect to the server",
            -2: "HTTP error occurred",
            -3: "too many redirects",
            -4: "the request timed out"
        }
        return err_dict[self.return_code]


def http_request(method: str, url: str, **kwargs) -> HttpResponse:
    resp = None
    try:
        if method.upper() == "GET":
            r = requests.get(url, **kwargs)
        elif method.upper() == "POST":
            r = requests.post(url, **kwargs)

        else:
            if method.upper() in ("PUT", "DELETE", "PUT"):
                raise NotImplementedError(f"{method} is not implemented.")
            else:
                raise ValueError(f"{method} is not a valid method.")
        try:
            resp = r.json()
        except requests.exceptions.JSONDecodeError:
            resp = r.text
        ret_val = r.status_code
    except requests.ConnectionError:
        ret_val = -1
    except requests.HTTPError:
        ret_val = -2
    except requests.TooManyRedirects:
        ret_val = -3
    except requests.Timeout:
        ret_val = -4
    except requests.RequestException:
        ret_val = -5
    return HttpResponse(resp, ret_val)


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
    # TODO: see issue #10
    url = "http://localhost:11434/api/tags"
    r = http_request("GET", url, timeout=0.3)
    if r.is_error():
        output.print_error(
            "failed to list available local AI models. Is ollama running?")
        return []
    r = r.response["models"]
    return [model["name"] for model in r]


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
    url = "http://localhost:11434/api/generate"
    out = http_request("POST", url, json=payload)
    if out.is_error():
        output.print_error(
            f"Failed to load {model_name}. Is ollama running?")
        return {}
    return out.response


def unload_model() -> None:
    """
    Unload the local model from RAM
    """
    global selected_model
    url = "http://localhost:11434/api/generate"
    payload = {"model": selected_model, "keep_alive": 0}
    selected_model = None
    out = http_request("POST", url, json=payload)


# TODO: see issues #11 and #15
def generate() -> None:
    """
    generate commit message
    """
    url = "http://localhost:11434/api/generate"
    diff = git_utils.get_clean_diff()
    if diff == "":
        output.print_warning("No changes to the repository.")
        return
    payload = {"model": selected_model, "prompt": generation_prompt + diff,
               "stream": False}
    r = http_request("POST", url, json=payload)

    r = output.wrap_text(r.response.get("response").strip(), 72)

    global gen_message
    gen_message = r

    output.print_generated(r)


def regenerate(prompt: str) -> None:
    """
    regenerate commit message based on prompt
    """
    pass
