import re
import sys
import textwrap
from pathlib import Path

USAGE = textwrap.dedent(
    """\
    python fix_links.py FILENAME [FILENAME...]

        Attempt to fix links in accordance with a predefined list of rules.
        You must specify at least one FILENAME. Note that filenames are
        treated as glob patterns relative to the working directory. After
        any glob returns, we will filter for filenames that end in `.md`.
"""
)


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


def main():
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    cwd = Path(".")
    for pattern in sys.argv[1:]:
        for path in cwd.glob(pattern):
            if path.is_dir():
                # We skip directories
                continue

            if path.suffix == ".md":
                fixed_md = fix_md(path)
                with open(path, "wt") as outfile:
                    outfile.write(fixed_md)
            else:
                print(f"Skipping {path} as it is not an md")


if __name__ == "__main__":
    main()
