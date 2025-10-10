import nox

venv: str = "uv|virtualenv"


@nox.session(reuse_venv=True, venv_backend=venv)
def install(session):
    """
    Set up the development environment.
    """
    session.install("-e", ".[dev]")


@nox.session(reuse_venv=True, venv_backend=venv)
def lint(session):
    """
    ruff check . && mypy .
    """
    session.run("ruff", "check", ".")
    session.run("mypy", ".")


@nox.session(reuse_venv=True, venv_backend=venv)
def test(session):
    """
    pytest
    """
    session.run("pytest")


@nox.session(reuse_venv=True, venv_backend=venv)
def format(session):  # noqa: A001
    """
    ruff format .
    """
    session.run("ruff", "format", ".")
