"""
This file assumes that: ollama and git are installed, we are inside a git
working tree (in the git repo, not the .git folder), and the ollama server is
correctly working and ready to generate a message.
"""

import subprocess

import pytest


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
        text=True,
        input=user_in,
        timeout=5,
    )
    assert out.returncode == 0
    assert out.stderr.strip() == ""
