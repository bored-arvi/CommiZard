import subprocess
from unittest.mock import patch

import pytest
from commizard import git_utils


@pytest.mark.parametrize(
    "args, mock_result, side_effect",
    [
        # Successful git commands
        (["status"],
         subprocess.CompletedProcess(args=["git", "status"], returncode=0,
                                     stdout="On branch main\n", stderr=""),
         None),
        (["log", "--oneline"],
         subprocess.CompletedProcess(args=["git", "log", "--oneline"],
                                     returncode=0,
                                     stdout="abc123 Initial commit\n",
                                     stderr=""), None),
        # Git command failure
        (["push"],
         subprocess.CompletedProcess(args=["git", "push"], returncode=1,
                                     stdout="", stderr="Authentication failed"),
         None),
        # Exceptions
        (["status"], None, FileNotFoundError("git not found")),
        (["push"], None,
         subprocess.TimeoutExpired(cmd=["git", "push"], timeout=5)),
    ]
)
@patch("subprocess.run")
def test_run_git_command_all_cases(mock_run, args, mock_result, side_effect):
    if side_effect:
        mock_run.side_effect = side_effect
        with pytest.raises(type(side_effect)):
            git_utils.run_git_command(args)

    # if the test case didn't raise an exception
    else:
        mock_run.return_value = mock_result
        result = git_utils.run_git_command(args)

        # was subprocess.run called with correct arguments
        mock_run.assert_called_once_with(
            ["git"] + args,
            capture_output=True,
            text=True
        )

        assert result is mock_result
