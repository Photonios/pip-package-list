import os

from dataclasses import dataclass
from typing import Generator, List, Optional


@dataclass
class RequirementsEntrySource:
    path: str
    line: Optional[str]
    line_number: Optional[str]


@dataclass
class RequirementsEntry:
    source: Optional[RequirementsEntrySource]


@dataclass
class RequirementsRecursiveEntry(RequirementsEntry):
    path: str


@dataclass
class RequirementsEditableEntry(RequirementsEntry):
    path: str


@dataclass
class RequirementsVCSPackageEntry(RequirementsEntry):
    vcs: str
    uri: str
    tag: Optional[str]


@dataclass
class RequirementsPackageEntry(RequirementsEntry):
    name: str
    operator: str
    version: str


def parse_requirements(
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

        # TODO: add support for other VCS's
        elif stripped_line.startswith("git+"):
            yield parse_vcs_requirements_entry(line_source, stripped_line)
        else:
            yield parse_package_requirements_entry(line_source, stripped_line)


def parse_recursive_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsRecursiveEntry:
    path = _clean_line(line.replace("-r", ""))
    return RequirementsRecursiveEntry(
        source=source,
        path=os.path.realpath(os.path.join(os.path.dirname(source.path), path)),
    )


def parse_editable_requirements_entry(
    source: RequirementsEntrySource, line: str
) -> RequirementsEditableEntry:
    path = _clean_line(line.replace("-e", ""))
    return RequirementsEditableEntry(
        source=source,
        path=os.path.realpath(os.path.join(os.path.dirname(source.path), path)),
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


def _clean_line(line: str) -> str:
    return line.strip().replace("\n", "").replace("\r", "")
