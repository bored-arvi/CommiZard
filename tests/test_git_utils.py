import subprocess
from unittest.mock import patch

import pytest
from commizard import git_utils


# TODO: add valid test cases that mock actual returns or subprocess.run
@pytest.mark.parametrize(
    "args, mock_result, raised_exception",
    [
        # successful git commands
        (["status"],
         subprocess.CompletedProcess(args=["git", "status"], returncode=0,
                                     stdout="On branch main\n", stderr=""),
         None),
        (["log", "--oneline"],
         subprocess.CompletedProcess(args=["git", "log", "--oneline"],
                                     returncode=0,
                                     stdout="abc123 Initial commit\n",
                                     stderr=""), None),
        # git command failure
        (["push"],
         subprocess.CompletedProcess(args=["git", "push"], returncode=1,
                                     stdout="", stderr="Authentication failed"),
         None),
        # exceptions
        (["status"], None, FileNotFoundError("git not found")),
        (["push"], None,
         subprocess.TimeoutExpired(cmd=["git", "push"], timeout=5)),
    ]
)
@patch("subprocess.run")
def test_run_git_command(mock_run, args, mock_result, raised_exception):
    if raised_exception:
        mock_run.side_effect = raised_exception

    # if the test case didn't raise an exception
    else:
        mock_run.return_value = mock_result

    result = git_utils.run_git_command(args)

    # was subprocess.run called with correct arguments
    mock_run.assert_called_once_with(["git"] + args, capture_output=True,
                                     text=True)

    assert result is mock_result


@pytest.mark.parametrize(
    "mock_val, expected_result",
    [
        (subprocess.CompletedProcess(
            args=['git', 'rev-parse', '--is-inside-work-tree'],
            returncode=128, stdout='',
            stderr='fatal: not a git repository (or any of the parent directories): .git\n'),
         False),
        (subprocess.CompletedProcess(
            args=['git', 'rev-parse', '--is-inside-work-tree'], returncode=0,
            stdout='true\n', stderr=''), True),
        (subprocess.CompletedProcess(
            args=['git', 'rev-parse', '--is-inside-work-tree'], returncode=0,
            stdout='false\n', stderr=''), False),
    ]
)
@patch("commizard.git_utils.run_git_command")
def test_is_inside_working_tree(mock_run, mock_val, expected_result):
    mock_run.return_value = mock_val
    res: bool = git_utils.is_inside_working_tree()
    mock_run.assert_called_once_with(["rev-parse", "--is-inside-work-tree"])
    assert res == expected_result
