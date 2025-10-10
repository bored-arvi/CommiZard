"""
This file assumes that: ollama and git are installed, we are inside a git
working tree (in the git repo, not the .git folder), and the ollama server is
correctly working and ready to generate a message.
"""

import os
import subprocess

import pytest

# Don't mess up the encoding of colored output
env = {**os.environ, "PYTHONIOENCODING": "utf-8"}


@pytest.mark.parametrize(
    "user_in",
    [
        "       quit            \n",
        "exit\n",
        " exit\n",
    ],
)
def test_early_exit(user_in):
    out = subprocess.run(
        ["commizard"],
        capture_output=True,
        input=user_in.encode(),
        timeout=5,
        env=env,
    )
    assert out.returncode == 0
    assert out.stderr.decode("utf-8").strip() == ""


@pytest.mark.parametrize(
    "user_in",
    [
        ["clear", "list", "start something", "gen", "exit"],
        ["start something", "gen", "quit"],
        ["gen", "quit"],
    ],
)
def test_correct_workflow(user_in):
    user_in = "\n".join(user_in) + "\n"
    out = subprocess.run(
        ["commizard"], capture_output=True, input=user_in.encode(), env=env
    )
    assert out.returncode == 0
