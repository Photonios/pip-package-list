import os

from pippackagelist.requirements import (
    RequirementsEditableEntry,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
)
from pippackagelist.setup_py_parser import parse_setup_py

setup_py_path = os.path.join(os.path.dirname(__file__), "./test-cases/setup.py")
setup_py_with_extras_path = os.path.join(
    os.path.dirname(__file__), "./test-cases/setup_with_extras.py"
)


def test_parse_setup_py():
    requirements = list(parse_setup_py(setup_py_path))
    assert len(requirements) == 4

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert isinstance(requirements[1], RequirementsPackageEntry)
    assert isinstance(requirements[2], RequirementsRecursiveEntry)
    assert isinstance(requirements[3], RequirementsEditableEntry)

    for index, requirement in enumerate(requirements):
        assert requirement.source.path == os.path.realpath(setup_py_path)
        assert requirement.source.line_number == index + 1


def test_parse_setup_py_with_extras():
    requirements = list(parse_setup_py(setup_py_with_extras_path))
    assert len(requirements) == 3

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert requirements[0].name == "django"
    assert requirements[0].version == "1.0"
    assert requirements[0].operator == "=="

    assert isinstance(requirements[1], RequirementsPackageEntry)
    assert requirements[1].name == "pytest"
    assert requirements[1].version == "2.0"
    assert requirements[1].operator == "=="

    assert isinstance(requirements[2], RequirementsPackageEntry)
    assert requirements[2].name == "Sphinx"
    assert requirements[2].version == "1.0"
    assert requirements[2].operator == "=="
