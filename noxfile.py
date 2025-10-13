import nox  # type: ignore

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
    run unit tests. returns coverage report if "cov" posarg is sent
    """
    session.install("pytest")
    if "cov" in session.posargs:
        session.install("pytest-cov")
        args = ("pytest", "--cov=commizard", "-q", "./tests/unit")
    else:
        args = ("pytest", "-q", "./tests/unit")
    session.run(*args)


@nox.session(reuse_venv=True, venv_backend=venv)
def format(session):  # noqa: A001
    """
    ruff format .
    """
    session.install("ruff")
    session.run("ruff", "format", ".")


@nox.session(reuse_venv=True, venv_backend=venv)
def e2e_test(session):
    """
    run e2e tests (Warning: It's slow)
    """
    session.install("pytest")
    session.run("pytest", "-q", "./tests/e2e")


@nox.session(reuse_venv=True, venv_backend=venv)
def check(session):
    """
    run formatter, linter and shallow tests
    """
    session.notify("format")
    session.notify("lint")
    session.notify("test")


@nox.session(reuse_venv=True, venv_backend=venv)
def check_all(session):
    """
    run all checks (used in CI. Use the check session for a faster check)
    """
    session.notify("format")
    session.notify("lint")
    session.notify("test", ["cov"])
    session.notify("e2e_test")
