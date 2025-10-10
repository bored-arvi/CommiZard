"""
This file assumes that: ollama and git are installed, we are inside a git
working tree (in the git repo, not the .git folder), and the ollama server is
correctly working and ready to generate a message.
"""

import os
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
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    out = subprocess.run(
        ["commizard"],
        capture_output=True,
        input=user_in.encode(),
        timeout=5,
        env=env,
    )
    assert out.returncode == 0
    assert out.stderr.decode("utf-8").strip() == ""
