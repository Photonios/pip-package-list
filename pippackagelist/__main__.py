import sys

from .requirements import RequirementsEditableEntry, RequirementsRecursiveEntry
from .requirements_txt_parser import parse_requirements_txt
from .setup_py_parser import parse_setup_py


def main() -> int:
    input_file = sys.argv[1]

    aggregated_entries = []
    for requirement in parse_requirements_txt(input_file):
        if isinstance(requirement, RequirementsRecursiveEntry):
            aggregated_entries.extend(
                list(parse_requirements_txt(requirement.path))
            )
        elif isinstance(requirement, RequirementsEditableEntry):
            aggregated_entries.extend(list(parse_setup_py(requirement.path)))
        else:
            aggregated_entries.append(requirement)

    for req in aggregated_entries:
        print(req.source.line, req.source.path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
