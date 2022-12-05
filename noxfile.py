import nox


@nox.session
def tests(session):
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.install("pytest")
    session.run("pytest", *session.posargs)
