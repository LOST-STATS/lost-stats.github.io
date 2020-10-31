import pytest

from lostutils.constants import PYTHON_DOCKER_IMAGE, R_DOCKER_IMAGE


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
        "--docker-python",
        action="store",
        default=PYTHON_DOCKER_IMAGE,
        help="The tag of the docker image to use for Python tests",
    )

    parser.addoption(
        "--docker-r",
        action="store",
        default=R_DOCKER_IMAGE,
        help="The tag of the docker image to use for R tests",
    )


@pytest.fixture
def python_docker_image(request) -> str:
    return request.config.getoption("--docker-python")


@pytest.fixture
def r_docker_image(request) -> str:
    return request.config.getoption("--docker-r")
