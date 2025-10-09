import nox


@nox.session
def install(session):
    """
    Set up the development environment.
    """
    session.install("-e", ".[dev]")


@nox.session
def lint(session):
    """
    ruff check . && mypy .
    """
    session.install("ruff", "mypy")
    session.run("ruff", "check", ".")
    session.run("mypy", ".")


@nox.session
def test(session):
    """
    pytest
    """
    session.install("pytest", "pytest-cov")
    session.run("pytest")


@nox.session
def format(session):
    """
    ruff format .
    """
    session.install("ruff")
    session.run("ruff", "format", ".")
