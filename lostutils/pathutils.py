from pathlib import Path
from typing import List, Union


def expand_filenames(
    filenames: List[Union[str, Path]], cwd: Path = Path(".")
) -> List[Path]:
    """
    Given a list of filenames, initially treat them as glob patterns. If a
    directory appears among them, glob it again with the pattern '**/*.md'.
    Finally, filter out the list for only .md files.

    Args:
        filenames: The list of filenames to expand
        cwd: The current working diretory relative to which the filenames are

    Returns:
        The list of expanded filenames, sorted.
    """
    new_filenames = []
    for filename in filenames:
        if any(char in str(filename) for char in ['*', '?', '[']):
            # This is a glob
            new_filenames.extend(cwd.glob(filename))
        else:
            new_filenames.append(cwd / filename)

    output: List[Path] = []
    for filename in new_filenames:
        if filename.is_dir():
            output.extend(filename.glob("**/*.md"))
        elif filename.exists() and filename.suffix == ".md":
            output.append(filename)

    output = [filename for filename in output if filename.exists()]
    return sorted(output)


def expand_and_filter_filenames(
    filenames: List[Union[str, Path]],
    skip_filenames: List[Union[str, Path]],
    cwd: Path = Path("."),
) -> List[Path]:
    filenames = expand_filenames(filenames, cwd=cwd)
    skip_filenames = expand_filenames(skip_filenames, cwd=cwd)
    return sorted(set(filenames) - set(skip_filenames))
