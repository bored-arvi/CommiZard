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
    session.install("ruff", "mypy")
    session.run("ruff", "check", ".")
    session.run("mypy", ".")


@nox.session(reuse_venv=True, venv_backend=venv)
def test(session):
    """
    pytest
    """
    session.install("pytest", "pytest-cov")
    session.run("pytest")


@nox.session(reuse_venv=True, venv_backend=venv)
def format(session):
    """
    ruff format .
    """
    session.install("ruff")
    session.run("ruff", "format", ".")
