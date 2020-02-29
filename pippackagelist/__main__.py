import sys

from .setup_py_parser import parse_setup_py
from .requirements_txt_parser import parse_requirements_txt
from .requirements import RequirementsRecursiveEntry, RequirementsEditableEntry


def main() -> int:
    input_file = sys.argv[1]

    aggregated_entries = []
    for requirement in parse_requirements_txt(input_file):
        if isinstance(requirement, RequirementsRecursiveEntry):
            aggregated_entries.extend(list(parse_requirements_txt(requirement.path)))
        elif isinstance(requirement, RequirementsEditableEntry):
            aggregated_entries.extend(list(parse_setup_py(requirement.path)))
        else:
            aggregated_entries.append(requirement)

    print(aggregated_entries)
    return 0


if __name__ == "__main__":
    sys.exit(main())
