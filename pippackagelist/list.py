from typing import Generator, List

from .identify_package_list_file_type import (
    PackageListFileType,
    identify_package_list_file_type,
)
from .requirements import (
    RequirementsEditableEntry,
    RequirementsEntry,
    RequirementsRecursiveEntry,
)
from .requirements_txt_parser import parse_requirements_txt
from .setup_py_parser import parse_setup_py


def list(
    file_paths: List[str],
    recurse_recursive: bool = True,
    recurse_editable: bool = True,
) -> Generator[RequirementsEntry, None, None]:
    generators = []

    for file_path in file_paths:
        package_list_file_type = identify_package_list_file_type(file_path)
        if package_list_file_type == PackageListFileType.REQUIREMENTS_TXT:
            generators.append(parse_requirements_txt(file_path))
        elif package_list_file_type == PackageListFileType.SETUP_PY:
            generators.append(parse_setup_py(file_path))

    while len(generators) > 0:
        for requirement in generators[0]:
            if isinstance(requirement, RequirementsRecursiveEntry):
                if recurse_recursive:
                    generators.append(
                        parse_requirements_txt(requirement.absolute_path)
                    )
                else:
                    yield requirement
            elif isinstance(requirement, RequirementsEditableEntry):
                if recurse_editable:
                    generators.append(
                        parse_setup_py(requirement.resolved_absolute_path)
                    )
                else:
                    yield requirement
            else:
                yield requirement

        generators = generators[1:]
