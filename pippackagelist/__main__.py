import argparse
import sys

from .list_packages_from_files import list_packages_from_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recurse-recursive",
        default=False,
        help="recurse into -r entries",
        action="store_true",
    )
    parser.add_argument(
        "--recurse-editable",
        default=False,
        help="recurse into -e entries",
        action="store_true",
    )
    parser.add_argument(
        "file_paths",
        nargs="+",
        help="list of requirements.txt or setup.py files",
    )

    args = parser.parse_args()

    for requirement in list_packages_from_files(
        args.file_paths,
        recurse_recursive=args.recurse_recursive,
        recurse_editable=args.recurse_editable,
    ):
        print(requirement)

    return 0


if __name__ == "__main__":
    sys.exit(main())
