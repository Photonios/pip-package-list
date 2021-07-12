import os
import re

from typing import Generator, List, Optional, Tuple
from urllib.parse import urlparse

from .entry import (
    RequirementsConstraintsEntry,
    RequirementsDirectRefEntry,
    RequirementsEditableEntry,
    RequirementsEntry,
    RequirementsEntrySource,
    RequirementsIndexURLEntry,
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

        elif requirement.startswith("-c"):
            yield parse_constraints_requirements_entry(
                line_source, requirement, extras, markers
            )

        elif requirement.startswith("-e"):
            yield parse_editable_requirements_entry(
                line_source, requirement, extras, markers
            )

        elif requirement.startswith("-i"):
            yield parse_index_url_requirements_entry(
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

        elif re.match(r"^(http|https|file)://(.+).whl", requirement):
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


def parse_constraints_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsConstraintsEntry:
    original_path = _clean_line(requirement.replace("-c", ""))
    absolute_path = os.path.realpath(
        os.path.join(os.path.dirname(source.path), original_path)
    )

    return RequirementsConstraintsEntry(
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


def parse_index_url_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsIndexURLEntry:
    url = _clean_line(requirement.replace("-i", ""))
    return RequirementsIndexURLEntry(source=source, url=url)


def parse_vcs_requirements_entry(
    source: RequirementsEntrySource,
    requirement: str,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsVCSPackageEntry:
    vcs, uri = requirement.split("+", maxsplit=1)

    # If this looks like a normal URL, let's use urlparse. We need to do this
    # so we can tell the username and tag apart, which both use '@'
    match = re.match(r"^(.+)://", uri)
    if match:
        uri_parts = urlparse(uri)

        name = None
        if "egg=" in uri_parts.fragment:
            name = uri_parts.fragment.replace("egg=", "")
            uri_parts = uri_parts._replace(
                fragment=uri_parts.fragment.replace(f"egg={name}", "")
            )

        tag = None
        if "@" in uri_parts.path:
            path, tag = uri_parts.path.split("@", maxsplit=1)
            uri_parts = uri_parts._replace(path=path)

        uri = uri_parts.geturl()

        return RequirementsVCSPackageEntry(
            source=source, vcs=vcs, uri=uri, tag=tag, name=name
        )

    # We're dealing with a Git SSH uri: git@github.com:/repo.git@tag@egg=name
    name = None
    if "#egg=" in uri:
        uri, name = uri.split("#egg=", maxsplit=1)

    tag = None

    repo_name_index = uri.rfind(":")
    if repo_name_index >= 0:
        repo_name = uri[repo_name_index:]
        if "@" in repo_name:
            uri, tag = uri.rsplit("@", maxsplit=1)

    return RequirementsVCSPackageEntry(
        source=source, vcs=vcs, uri=uri, tag=tag, name=name
    )


def parse_wheel_requirements_entry(
    source: RequirementsEntrySource,
    requirement,
    extras: List[str],
    markers: Optional[str] = None,
) -> RequirementsWheelPackageEntry:
    uri = requirement
    name = None

    if "#egg=" in requirement:
        uri, name = requirement.split("#egg=")

    return RequirementsWheelPackageEntry(
        source=source, uri=uri, name=name, markers=markers
    )


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
