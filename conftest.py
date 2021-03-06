def pytest_addoption(parser):
    parser.addoption(
        "--mdpath",
        action="append",
        default=[],
        help="List of md files (or directories containing md files) to search for code blocks in",
    )

    parser.addoption(
        "--xmdpath",
        action="append",
        default=[],
        help="List of md files (or directories containing md files) to explicitly *skip* the code blocks in",
    )

    parser.addoption(
        "--language",
        action="append",
        default=[],
        help="List of languages whose code samples to run (default is all)",
    )
