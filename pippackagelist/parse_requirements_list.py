import os
import re

from typing import Generator, List, Optional

from .entry import (
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

        if stripped_line.startswith("-r"):
            yield parse_recursive_requirements_entry(line_source, stripped_line)

        elif stripped_line.startswith("-e"):
            yield parse_editable_requirements_entry(line_source, stripped_line)

        elif re.match(r"^(.+)\+", stripped_line):
            yield parse_vcs_requirements_entry(line_source, stripped_line)

        elif stripped_line.endswith("whl"):
            yield parse_wheel_requirements_entry(line_source, stripped_line)

        else:
            yield parse_package_requirements_entry(line_source, stripped_line)


def parse_recursive_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsRecursiveEntry:
    original_path = _clean_line(line.replace("-r", ""))
    absolute_path = os.path.realpath(
        os.path.join(os.path.dirname(source.path), original_path)
    )

    return RequirementsRecursiveEntry(
        source=source, original_path=original_path, absolute_path=absolute_path,
    )


def parse_editable_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsEditableEntry:
    original_path = _clean_line(line.replace("-e", ""))
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
    )


def parse_vcs_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsVCSPackageEntry:
    vcs_uri_split = line.split("+")
    vcs = vcs_uri_split[0]

    uri_tag_split = vcs_uri_split[1].split("#")
    uri = uri_tag_split[0]

    tag = None
    if len(uri_tag_split) > 1:
        tag = uri_tag_split[1]

    return RequirementsVCSPackageEntry(source=source, vcs=vcs, uri=uri, tag=tag)


def parse_wheel_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsWheelPackageEntry:
    return RequirementsWheelPackageEntry(source=source, uri=line,)


def parse_package_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsPackageEntry:
    operators = ["==", ">=", ">", "<=", "<"]
    for operator in operators:
        parts = line.split(operator)
        if len(parts) == 1:
            continue

        return RequirementsPackageEntry(
            source=source, name=parts[0], operator=operator, version=parts[1]
        )

    raise RequirementsEntryParseError(
        f"cannot parse '{line}' in {source.path}:{source.line_number}"
    )


def _clean_line(line: str) -> str:
    return (
        line.strip()
        .replace("\n", "")
        .replace("\r", "")
        .replace("  ", " ")
        .replace("  ", " ")
    )
