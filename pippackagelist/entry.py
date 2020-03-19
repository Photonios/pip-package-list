import os

from dataclasses import dataclass
from typing import Optional


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
    original_path: str
    absolute_path: str

    def __str__(self) -> str:
        path = os.path.relpath(self.absolute_path, os.getcwd())
        return f"-r {path}"


@dataclass
class RequirementsEditableEntry(RequirementsEntry):
    original_path: str
    absolute_path: str

    resolved_path: str
    resolved_absolute_path: str

    def __str__(self) -> str:
        path = os.path.relpath(self.absolute_path, os.getcwd())
        return f"-e {path}"


@dataclass
class RequirementsVCSPackageEntry(RequirementsEntry):
    vcs: str
    uri: str
    tag: Optional[str]

    def __str__(self) -> str:
        result = f"{self.vcs}+{self.uri}"
        if self.tag:
            result += f"#{self.tag}"

        return result


@dataclass
class RequirementsWheelPackageEntry(RequirementsEntry):
    uri: str

    def __str__(self) -> str:
        return self.uri


@dataclass
class RequirementsPackageEntry(RequirementsEntry):
    name: str
    operator: str
    version: str

    def __str__(self) -> str:
        return f"{self.name}{self.operator}{self.version}"
