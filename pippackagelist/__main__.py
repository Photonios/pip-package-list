import argparse
import sys

from .entry import (
    RequirementsEditableEntry,
    RequirementsRecursiveEntry,
    RequirementsVCSPackageEntry,
    RequirementsWheelPackageEntry,
)
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
        "--dedupe",
        default=False,
        help="de-duplicate the resulting list",
        action="store_true",
    )
    parser.add_argument(
        "--remove-editable",
        default=False,
        help="remove editable requirements from the final list",
        action="store_true",
    )
    parser.add_argument(
        "--remove-recursive",
        default=False,
        help="remove recursive requirements from the final list",
        action="store_true",
    )
    parser.add_argument(
        "--remove-vcs",
        default=False,
        help="remove vcs requirements from the final list",
        action="store_true",
    )
    parser.add_argument(
        "--remove-wheel",
        default=False,
        help="remove wheel requirements from the final list",
        action="store_true",
    )
    parser.add_argument(
        "file_paths",
        nargs="+",
        help="list of requirements.txt or setup.py files",
    )

    args = parser.parse_args()

    reqs = list_packages_from_files(
        args.file_paths,
        recurse_recursive=args.recurse_recursive,
        recurse_editable=args.recurse_editable,
    )

    if args.remove_editable:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsEditableEntry)
        ]

    if args.remove_recursive:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsRecursiveEntry)
        ]

    if args.remove_vcs:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsVCSPackageEntry)
        ]

    if args.remove_wheel:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsWheelPackageEntry)
        ]

    if args.dedupe:
        deduped_reqs = list(set([str(requirement) for requirement in reqs]))
        for requirement in deduped_reqs:
            print(requirement)
    else:
        for requirement in reqs:
            print(requirement)

    return 0


if __name__ == "__main__":
    sys.exit(main())
