import os

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RequirementsEntrySource:
    path: str
    line: Optional[str] = None
    line_number: Optional[str] = None


@dataclass
class RequirementsEntry:
    source: Optional[RequirementsEntrySource]

    def package_name(self) -> Optional[str]:
        return None


@dataclass
class RequirementsRecursiveEntry(RequirementsEntry):
    original_path: str
    absolute_path: str

    def __str__(self) -> str:
        path = os.path.relpath(self.absolute_path, os.getcwd())
        return f"-r {path}"


@dataclass
class RequirementsConstraintsEntry(RequirementsEntry):
    original_path: str
    absolute_path: str

    def __str__(self) -> str:
        path = os.path.relpath(self.absolute_path, os.getcwd())
        return f"-c {path}"


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
class RequirementsIndexURLEntry(RequirementsEntry):
    url: str

    def __str__(self) -> str:
        return f"-i {self.url}"


@dataclass
class RequirementsVCSPackageEntry(RequirementsEntry):
    vcs: str
    uri: str
    tag: Optional[str] = None
    name: Optional[str] = None

    def package_name(self) -> Optional[str]:
        return self.name

    def __str__(self) -> str:
        result = f"{self.vcs}+{self.uri}"
        if self.tag:
            result += f"@{self.tag}"

        if self.name:
            result += f"#egg={self.name}"

        return result


@dataclass
class RequirementsWheelPackageEntry(RequirementsEntry):
    uri: str
    name: Optional[str] = None

    markers: Optional[str] = None

    def package_name(self) -> Optional[str]:
        return self.name

    def __str__(self) -> str:
        line = self.uri
        if self.name:
            line += f"#egg={self.name}"

        if self.markers:
            line += f" ; {self.markers}"

        return line


@dataclass
class RequirementsDirectRefEntry(RequirementsEntry):
    name: str
    uri: str

    markers: Optional[str] = None

    def package_name(self) -> Optional[str]:
        return self.name

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

    def package_name(self) -> Optional[str]:
        return self.name

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
