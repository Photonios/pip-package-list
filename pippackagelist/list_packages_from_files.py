from typing import Generator, List

from .entry import (
    RequirementsEditableEntry,
    RequirementsEntry,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
    RequirementsVCSPackageEntry,
    RequirementsWheelPackageEntry,
)
from .identify_package_list_file_type import (
    PackageListFileType,
    identify_package_list_file_type,
)
from .parse_requirements_txt import parse_requirements_txt
from .parse_setup_py import parse_setup_py


def _list_packages_from_files(
    file_paths: List[str],
    *,
    recurse_recursive: bool = False,
    recurse_editable: bool = False,
    remove_editable: bool = False,
    remove_recursive: bool = False,
    remove_vcs: bool = False,
    remove_wheel: bool = False,
    remove_unversioned: bool = False,
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
                elif not remove_recursive:
                    yield requirement
            elif isinstance(requirement, RequirementsEditableEntry):
                if recurse_editable:
                    generators.append(
                        parse_setup_py(
                            requirement.resolved_absolute_path,
                            requirement.extras,
                        )
                    )
                elif not remove_editable:
                    yield requirement
            elif isinstance(requirement, RequirementsVCSPackageEntry):
                if not remove_vcs:
                    yield requirement
            elif isinstance(requirement, RequirementsWheelPackageEntry):
                if not remove_wheel:
                    yield requirement
            elif isinstance(requirement, RequirementsPackageEntry):
                if remove_unversioned and not requirement.version:
                    continue
                else:
                    yield requirement

        generators = generators[1:]


def list_packages_from_files(
    file_paths: List[str],
    *,
    recurse_recursive: bool = False,
    recurse_editable: bool = False,
    remove_editable: bool = False,
    remove_recursive: bool = False,
    remove_vcs: bool = False,
    remove_wheel: bool = False,
    remove_unversioned: bool = False,
    dedupe: bool = False,
) -> Generator[RequirementsEntry, None, None]:
    generator = _list_packages_from_files(
        file_paths,
        recurse_recursive=recurse_recursive,
        recurse_editable=recurse_editable,
        remove_editable=remove_editable,
        remove_recursive=remove_recursive,
        remove_vcs=remove_vcs,
        remove_wheel=remove_wheel,
        remove_unversioned=remove_unversioned,
    )

    if not dedupe:
        for req in generator:
            yield req
        return

    unique_requirements = []
    unique_requirements_strings = set()
    for requirement in generator:
        if str(requirement) in unique_requirements_strings:
            continue

        unique_requirements.append(requirement)
        unique_requirements_strings.add(str(requirement))

    for requirement in unique_requirements:
        yield requirement
