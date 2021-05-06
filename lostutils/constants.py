import os


# What docker image should Python code be executed in?
PYTHON_DOCKER_IMAGE = os.environ.get(
    "LOST_PYTHON_DOCKER_IMAGE", "ghcr.io/lost-stats/docker-images/tester-python:latest"
)

# What docker image should R code be executed in?
R_DOCKER_IMAGE = os.environ.get(
    "LOST_R_DOCKER_IMAGE", "ghcr.io/lost-stats/docker-images/tester-r:latest"
)
