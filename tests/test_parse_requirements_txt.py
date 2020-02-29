import os

from pippackagelist.requirements import (
    RequirementsEditableEntry,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
)
from pippackagelist.requirements_txt_parser import parse_requirements_txt

requirements_txt_path = os.path.join(
    os.path.dirname(__file__), "./test-cases/requirements.txt"
)


def test_parse_requirements_txt():
    requirements = list(parse_requirements_txt(requirements_txt_path))
    assert len(requirements) == 4

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert isinstance(requirements[1], RequirementsPackageEntry)
    assert isinstance(requirements[2], RequirementsRecursiveEntry)
    assert isinstance(requirements[3], RequirementsEditableEntry)

    for index, requirement in enumerate(requirements):
        assert requirement.source.path == os.path.realpath(
            requirements_txt_path
        )
        assert requirement.source.line_number == index + 1
