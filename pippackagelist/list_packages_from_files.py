from collections import defaultdict
from typing import Generator, List

from .entry import (
    RequirementsConstraintsEntry,
    RequirementsEditableEntry,
    RequirementsEntry,
    RequirementsIndexURLEntry,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
    RequirementsVCSPackageEntry,
    RequirementsWheelPackageEntry,
)
from .error import ConstraintWithoutNameError
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
    remove_constraints: bool = False,
    remove_vcs: bool = False,
    remove_wheel: bool = False,
    remove_unversioned: bool = False,
    remove_index_urls: bool = False,
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
            elif isinstance(requirement, RequirementsConstraintsEntry):
                if not remove_constraints:
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
            elif isinstance(requirement, RequirementsIndexURLEntry):
                if not remove_index_urls:
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


def _dedupe_requirements(
    generator: Generator[RequirementsEntry, None, None]
) -> Generator[RequirementsEntry, None, None]:
    """Removes exact duplicates from the list of requirements.

    Duplicates can happen as multiple files are merged together and they
    all reefer to the same dependency. De-duping should have no impact
    on the final result, it just makes the list easier to browse.
    """

    unique_requirements = []
    unique_requirements_strings = set()
    for requirement in generator:
        if str(requirement) in unique_requirements_strings:
            continue

        unique_requirements.append(requirement)
        unique_requirements_strings.add(str(requirement))

    for requirement in unique_requirements:
        yield requirement


def _inline_constraints(
    generator: Generator[RequirementsEntry, None, None]
) -> Generator[RequirementsEntry, None, None]:
    """Inlines constraints specified in constraint.txt files (specified by -c).

    Constraints override what version of a package should be installed. They cannot
    add new packages to the list. Any package in the constraints file that isn't
    already in the list is ignored.

    We have to be careful because the constraints file could contain multiple
    entries for the same package. Each entry could have different markers.

    Constraint files have the same syntax as requirements.txt files, but with
    some restrictions:

        * No nesting
        * No editables
        * All entries must have a name
    """

    requirements = []
    constraints = defaultdict(list)

    for requirement in generator:
        if not isinstance(requirement, RequirementsConstraintsEntry):
            requirements.append(requirement)
            continue

        for constraint in parse_requirements_txt(requirement.absolute_path):
            if constraint.package_name() is None:
                raise ConstraintWithoutNameError(constraint)

            constraints[constraint.package_name()].append(constraint)

    for requirement in requirements:
        if not requirement.package_name():
            yield requirement
            continue

        requirement_constraints = constraints.get(requirement.package_name())
        if requirement_constraints:
            for constraint in requirement_constraints:
                yield constraint
        else:
            yield requirement


def list_packages_from_files(
    file_paths: List[str],
    *,
    recurse_recursive: bool = False,
    recurse_editable: bool = False,
    inline_constraints: bool = False,
    remove_editable: bool = False,
    remove_recursive: bool = False,
    remove_constraints: bool = False,
    remove_vcs: bool = False,
    remove_wheel: bool = False,
    remove_unversioned: bool = False,
    remove_index_urls: bool = False,
    dedupe: bool = False,
) -> Generator[RequirementsEntry, None, None]:
    generator = _list_packages_from_files(
        file_paths,
        recurse_recursive=recurse_recursive,
        recurse_editable=recurse_editable,
        remove_editable=remove_editable,
        remove_recursive=remove_recursive,
        remove_constraints=remove_constraints,
        remove_vcs=remove_vcs,
        remove_wheel=remove_wheel,
        remove_unversioned=remove_unversioned,
        remove_index_urls=remove_index_urls,
    )

    if inline_constraints:
        generator = _inline_constraints(generator)

    if dedupe:
        generator = _dedupe_requirements(generator)

    for requirement in generator:
        yield requirement
