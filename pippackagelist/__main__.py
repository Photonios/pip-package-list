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
        "--inline-constraints",
        default=False,
        help="recurse into -c entries and inline them",
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
        help="remove recursive requirements (-r) from the final list",
        action="store_true",
    )
    parser.add_argument(
        "--remove-constraints",
        default=False,
        help="remove constaints (-c) from the final list",
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
        "--remove-unversioned",
        default=False,
        help="remove requirements without a version number from the final list",
        action="store_true",
    )
    parser.add_argument(
        "--remove-index-urls",
        default=False,
        help="remove -i entries (index urls) from the final list",
        action="store_true",
    )
    parser.add_argument(
        "file_paths",
        nargs="+",
        help="list of requirements.txt or setup.py files",
    )

    args = parser.parse_args()

    requirements = list_packages_from_files(
        args.file_paths,
        recurse_recursive=args.recurse_recursive,
        recurse_editable=args.recurse_editable,
        inline_constraints=args.inline_constraints,
        remove_editable=args.remove_editable,
        remove_recursive=args.remove_recursive,
        remove_constraints=args.remove_constraints,
        remove_vcs=args.remove_vcs,
        remove_wheel=args.remove_wheel,
        remove_unversioned=args.remove_unversioned,
        remove_index_urls=args.remove_index_urls,
        dedupe=args.dedupe,
    )

    for req in requirements:
        print(req)

    return 0


if __name__ == "__main__":
    sys.exit(main())
