from typing import Generator

from .requirements import parse_requirements, RequirementsEntry, RequirementsEntrySource


def parse_requirements_txt(file_path: str) -> Generator[RequirementsEntry, None, None]:
    source = RequirementsEntrySource(path=file_path, line=None, line_number=None)

    with open(file_path, 'r') as fp:
        for requirement in parse_requirements(source, fp.readlines()):
            yield requirement
