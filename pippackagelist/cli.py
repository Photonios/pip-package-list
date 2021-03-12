from typing import List

from .entry import (
    RequirementsEditableEntry,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
    RequirementsVCSPackageEntry,
    RequirementsWheelPackageEntry,
)
from .list_packages_from_files import list_packages_from_files


def run(
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
) -> List[str]:
    reqs = list_packages_from_files(
        file_paths,
        recurse_recursive=recurse_recursive,
        recurse_editable=recurse_editable,
    )

    if remove_editable:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsEditableEntry)
        ]

    if remove_recursive:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsRecursiveEntry)
        ]

    if remove_vcs:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsVCSPackageEntry)
        ]

    if remove_wheel:
        reqs = [
            requirement
            for requirement in reqs
            if not isinstance(requirement, RequirementsWheelPackageEntry)
        ]

    if remove_unversioned:
        versioned_reqs = []
        for requirement in reqs:
            if (
                isinstance(requirement, RequirementsPackageEntry)
                and not requirement.version
            ):
                continue

            versioned_reqs.append(requirement)

        reqs = versioned_reqs

    if dedupe:
        reqs = list(set([str(requirement) for requirement in reqs]))

    return reqs
