import os

from dataclasses import dataclass, field
from typing import List, Optional


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

    extras: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        line = os.path.relpath(self.absolute_path, os.getcwd())
        if self.extras:
            line += "[" + ",".join(self.extras) + "]"

        return f"-e {line}"


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
    markers: Optional[str] = None

    def __str__(self) -> str:
        line = self.uri
        if self.markers:
            line += f" ; {self.markers}"

        return line


@dataclass
class RequirementsDirectRefEntry(RequirementsEntry):
    name: str
    uri: str
    markers: Optional[str] = None

    def __str__(self) -> str:
        line = f"{self.name} @ {self.uri}"
        if self.markers:
            line += f" ; {self.markers}"

        return line


@dataclass
class RequirementsPackageEntry(RequirementsEntry):
    name: str
    extras: List[str] = field(default_factory=list)
    operator: Optional[str] = None
    version: Optional[str] = None
    markers: Optional[str] = None

    def __str__(self) -> str:
        line = self.name

        if self.extras:
            line += "[" + ",".join(self.extras) + "]"

        if self.operator:
            line += self.operator

        if self.version:
            line += self.version

        if self.markers:
            line += f"; {self.markers}"

        return line
