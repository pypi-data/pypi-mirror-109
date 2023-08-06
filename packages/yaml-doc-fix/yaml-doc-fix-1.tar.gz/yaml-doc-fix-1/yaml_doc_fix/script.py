import os
import glob
import subprocess
from pathlib import Path
from typing import List, Union


def run() -> None:
    """ Entry point for the script """
    walk_through_documents()


def walk_through_documents() -> None:
    files_to_ignore = read_gitignore()

    # Get all files in the ./ansible directory
    for subdir, dirs, filenames in os.walk("."):
        # Walk through all of them
        for filename in filenames:
            path = subdir + os.sep + filename

            # Skip non-yml files or *vault.yml files
            if not path.endswith('.yml')     \
               or path.endswith('vault.yml') \
               or path.strip("./") in files_to_ignore:
                continue

            # Run yamllint
            linter_output = run_linter(path)

            # If missing document start... prepend dashes
            if 'missing document start' in linter_output:
                print('Inserting document start to:', path)
                insert_document_start(path)


def read_gitignore() -> List[str]:
    """
    Read all files to ignore (from .gitignore)

    Returns:
        List[str]: files to ignore
    """
    files_to_ignore = []

    for p in Path("./.gitignore").read_text().split("\n"):
        if p and not p.startswith("#"):
            walk_gitignore(p, files_to_ignore)

    return files_to_ignore


def walk_gitignore(p: Union[Path, str], files_to_ignore: List[str]) -> None:
    """
    Reads a gitignore entry and appends it to the files_to_ignore list. If it is
    a directory, it will make sure to add all of their files and subdirs to the
    list as well.

    Args:
        p (Union[Path, str]): 
        files_to_ignore (List[str]): list of files
    """
    if Path(p).is_file():
        files_to_ignore.append(p)
    elif Path(p).is_dir():
        if p.endswith("/") or p.endswith("\\"):
            files_to_ignore.extend(glob.glob(p + "*"))
        else:
            files_to_ignore.extend(glob.glob(p + "/*"))
    else:
        for subdir in glob.glob(p):
            walk_gitignore(subdir, files_to_ignore)


def run_linter(path: Union[Path, str]) -> str:
    """
    Runs linter and returns its output.

    Args:
        path (Union[Path, str]): yaml document path

    Returns:
        str: linter's output
	"""
    proc = subprocess.run(
        'yamllint --strict ' + path,
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf8'
    )
    return proc.stdout


def insert_document_start(path: Path) -> str:
    """
    Inserts dashes at the beginning of the yaml document.
    Args:
        path (Path): document path.

    Returns:
        str: new contents of the file
    """
    # Read document
    p = Path(path)
    contents = p.read_text()

    # Prepend dashes and save changes
    contents = '---\n' + contents
    p.write_text(contents, encoding='utf8')

    return contents
