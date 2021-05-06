from pathlib import Path

from lostutils.constants import R_DOCKER_IMAGE
from lostutils.style import format_file


def test_fix_md(fixtures_path: Path):
    actual = format_file(fixtures_path / "input_bad_style.md")
    print("----- Actual formatted -----")
    print(actual)
    print("------ done actual formatted -----")
    with open(fixtures_path / "output_bad_style.md") as infile:
        expected = infile.read()

    assert actual == expected
