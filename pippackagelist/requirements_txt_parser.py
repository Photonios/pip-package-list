from typing import Generator

from .requirements import (
    RequirementsEntry,
    RequirementsEntrySource,
    parse_requirements,
)


def parse_requirements_txt(
    file_path: str,
) -> Generator[RequirementsEntry, None, None]:
    source = RequirementsEntrySource(
        path=file_path, line=None, line_number=None
    )

    with open(file_path, "r") as fp:
        for requirement in parse_requirements(source, fp.readlines()):
            yield requirement
