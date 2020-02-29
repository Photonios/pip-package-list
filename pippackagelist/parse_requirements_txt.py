import os

from typing import Generator

from .entry import RequirementsEntry, RequirementsEntrySource
from .parse_requirements_list import parse_requirements_list


def parse_requirements_txt(
    file_path: str,
) -> Generator[RequirementsEntry, None, None]:
    source = RequirementsEntrySource(
        path=os.path.realpath(file_path), line=None, line_number=None
    )

    with open(file_path, "r") as fp:
        for requirement in parse_requirements_list(source, fp.readlines()):
            yield requirement
