import re
from pathlib import Path


def fix_md(path: Path) -> str:
    """
    Given a file, read it and change all the links that look like::

        http[s]://lost-stats.github.io/blah

    into::

        {{ "/blah" | relative_url }}

    Args:
        path: The path to transform

    Returns:
        The transformed md file
    """
    with open(path, "rt") as infile:
        md_file = infile.read()

    return re.sub(
        r"http[s]://lost-stats.github.io(/[a-zA-Z0-9/#-&=+_%\.]*)",
        r'{{ "\1" | relative_url }}',
        md_file,
    )
