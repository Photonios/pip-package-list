import os
import re

from typing import Generator, List, Optional, Tuple

from .entry import (
    RequirementsDirectRefEntry,
    RequirementsEditableEntry,
    RequirementsEntry,
    RequirementsEntrySource,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
    RequirementsVCSPackageEntry,
    RequirementsWheelPackageEntry,
)


class RequirementsEntryParseError(RuntimeError):
    pass


def parse_requirements_list(
    source: Optional[RequirementsEntrySource], lines: List[str]
) -> Generator[RequirementsEntry, None, None]:

    for index, line in enumerate(lines):
        stripped_line = _clean_line(line)

        if not len(stripped_line) or stripped_line.startswith("#"):
            continue

        line_source = None
        if source:
            line_source = RequirementsEntrySource(
                path=source.path, line=stripped_line, line_number=index + 1
            )

        requirement, extras, markers = _split_requirement_and_markers(
            stripped_line
        )

        if requirement.startswith("-r"):
            yield parse_recursive_requirements_entry(
                line_source, requirement, extras, markers
            )

        elif requirement.startswith("-e"):
            yield parse_editable_requirements_entry(
                line_source, requirement, extras, markers
            )

        elif re.match(r"^(.+)\+", requirement):
            yield parse_vcs_requirements_entry(
                line_source, requirement, extras, markers
            )

        elif "@" in requirement:
            yield parse_direct_ref_requirements_entry(
                line_source, requirement, extras, markers,
            )

        elif requirement.endswith("whl"):
            yield parse_wheel_requirements_entry(
                line_source, requirement, extras, markers
            )

        else:
            yield parse_package_requirements_entry(
                line_source, requirement, extras, markers
            )


def parse_recursive_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsRecursiveEntry:
    original_path = _clean_line(requirement.replace("-r", ""))
    absolute_path = os.path.realpath(
        os.path.join(os.path.dirname(source.path), original_path)
    )

    return RequirementsRecursiveEntry(
        source=source, original_path=original_path, absolute_path=absolute_path,
    )


def parse_editable_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsEditableEntry:
    original_path = _clean_line(requirement.replace("-e", ""))
    resolved_path = original_path

    if not original_path.endswith(".py"):
        resolved_path = os.path.join(original_path, "setup.py")

    absolute_path = os.path.realpath(
        os.path.join(os.path.dirname(source.path), original_path)
    )
    resolved_absolute_path = os.path.realpath(
        os.path.join(os.path.dirname(source.path), resolved_path)
    )

    return RequirementsEditableEntry(
        source=source,
        original_path=original_path,
        absolute_path=absolute_path,
        resolved_path=resolved_path,
        resolved_absolute_path=resolved_absolute_path,
        extras=extras,
    )


def parse_vcs_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsVCSPackageEntry:
    vcs_uri_split = requirement.split("+")
    vcs = vcs_uri_split[0]

    uri_tag_split = vcs_uri_split[1].split("#")
    uri = uri_tag_split[0]

    tag = None
    if len(uri_tag_split) > 1:
        tag = uri_tag_split[1]

    return RequirementsVCSPackageEntry(source=source, vcs=vcs, uri=uri, tag=tag)


def parse_wheel_requirements_entry(
    source: RequirementsEntrySource,
    requirement,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsWheelPackageEntry:
    return RequirementsWheelPackageEntry(source=source, uri=requirement)


def parse_direct_ref_requirements_entry(
    source: RequirementsEntrySource,
    requirement,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsDirectRefEntry:
    name, uri = requirement.split("@")
    name = name.strip()
    uri = uri.strip()

    return RequirementsDirectRefEntry(
        source=source, name=name, uri=uri, markers=markers,
    )


def parse_package_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsPackageEntry:
    operators = ["==", ">=", ">", "<=", "<"]
    for operator in operators:
        parts = requirement.split(operator)
        if len(parts) == 1:
            continue

        return RequirementsPackageEntry(
            source=source,
            name=parts[0],
            extras=extras,
            operator=operator,
            version=parts[1],
            markers=markers,
        )

    return RequirementsPackageEntry(
        source=source, name=requirement, extras=extras, markers=markers,
    )


def _clean_line(line: str) -> str:
    return (
        line.strip()
        .replace("\n", "")
        .replace("\r", "")
        .replace("  ", " ")
        .replace("  ", " ")
    )


def _split_requirement_and_markers(
    line: str,
) -> Tuple[str, List[str], Optional[str]]:
    requirement = line
    markers = None
    extras = []

    if ";" in requirement:
        requirement, markers = requirement.split(";")

        requirement = requirement.strip()
        markers = markers.strip()

    extras_match = re.search(re.compile(r"\[.*\]"), requirement)
    if extras_match:
        matched_text = extras_match[0]

        requirement = requirement.replace(matched_text, "")
        extras = [
            extra.strip()
            for extra in matched_text.strip("[").strip("]").strip().split(",")
        ]

    return requirement, extras, markers
