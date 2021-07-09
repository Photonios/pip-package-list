import os

import pytest

from pippackagelist.entry import (
    RequirementsDirectRefEntry,
    RequirementsEditableEntry,
    RequirementsEntrySource,
    RequirementsIndexURLEntry,
    RequirementsPackageEntry,
    RequirementsRecursiveEntry,
    RequirementsVCSPackageEntry,
    RequirementsWheelPackageEntry,
)
from pippackagelist.parse_requirements_list import parse_requirements_list

source = RequirementsEntrySource(
    path="requirements.txt", line=None, line_number=None,
)


@pytest.mark.parametrize("path", ["../bla.txt", "./bla.txt", "/test.txt"])
def test_parse_requirements_recursive_entry(path):
    line = "-r %s" % path

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsRecursiveEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].absolute_path == os.path.realpath(
        os.path.join(os.getcwd(), path)
    )


@pytest.mark.parametrize("path", ["../bla", "./bla", "/mypackage", "."])
def test_parse_requirements_editable_entry(path):
    line = "-e %s" % path

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsEditableEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].absolute_path == os.path.realpath(
        os.path.join(os.getcwd(), path)
    )


def test_parse_requirements_editable_entry_with_extras():
    line = "-e ./mypackage[extra1, extra2]"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsEditableEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].absolute_path == os.path.realpath(
        os.path.join(os.getcwd(), "./mypackage")
    )
    assert requirements[0].extras == ["extra1", "extra2"]


@pytest.mark.parametrize("vcs", ["git", "hg"])
@pytest.mark.parametrize(
    "uri", ["https://github.com/org/repo", "git@github.com:org/repo.git"]
)
@pytest.mark.parametrize("tag", ["test", "1234", None])
def test_parse_requirements_vcs_package_entry(vcs, uri, tag):
    line = f"{vcs}+{uri}"
    if tag:
        line += f"#{tag}"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsVCSPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].vcs == vcs
    assert requirements[0].uri == uri
    assert requirements[0].tag == tag


@pytest.mark.parametrize("operator", ["==", ">=", ">", "<=", "<"])
def test_parse_requirements_package_entry(operator):
    line = "django%s1.0" % operator

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "django"
    assert requirements[0].version == "1.0"
    assert requirements[0].operator == operator
    assert not requirements[0].markers


def test_parse_requirements_package_entry_no_operator():
    line = "django"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "django"
    assert not requirements[0].version
    assert not requirements[0].operator
    assert not requirements[0].markers


def test_parse_requirements_package_entry_with_markers():
    line = 'django==1.2; sys_platform == "linux" and python_version < "3.9"'

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "django"
    assert requirements[0].version == "1.2"
    assert requirements[0].operator == "=="
    assert (
        requirements[0].markers
        == 'sys_platform == "linux" and python_version < "3.9"'
    )


def test_parse_requirements_package_entry_with_extras():
    line = "django[extra1, extra2]==1.2"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "django"
    assert requirements[0].extras == ["extra1", "extra2"]
    assert requirements[0].version == "1.2"
    assert requirements[0].operator == "=="
    assert not requirements[0].markers


def test_parse_requirements_wheel_package_entry():
    line = "https://mywebsite.com/mywheel.whl"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsWheelPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].uri == "https://mywebsite.com/mywheel.whl"
    assert not requirements[0].markers


def test_parse_requirements_direct_ref_package_entry():
    line = "mypackage @ https://website.com/mypackage.zip"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsDirectRefEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "mypackage"
    assert requirements[0].uri == "https://website.com/mypackage.zip"
    assert not requirements[0].markers


def test_parse_requirements_direct_ref_package_entry_with_markers():
    line = 'mypackage @ https://website.com/mypackage.zip ; sys_platform == "win32"'

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsDirectRefEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "mypackage"
    assert requirements[0].uri == "https://website.com/mypackage.zip"
    assert requirements[0].markers == 'sys_platform == "win32"'


def test_parse_requirements_index_url():
    line = "-i https://mypackages.com/repo/pypi"

    requirements = list(parse_requirements_list(source, [line]))
    assert len(requirements) == 1

    assert isinstance(requirements[0], RequirementsIndexURLEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == line
    assert requirements[0].source.line_number == 1
    assert requirements[0].url == "https://mypackages.com/repo/pypi"


def test_parse_requirements_skips_comments_and_blank_lines():
    lines = [
        "# this is a comment",
        "",
        "django==1.0",
        "    ",
        "   # another comment",
    ]

    requirements = list(parse_requirements_list(source, lines))
    assert len(requirements) == 1
    assert isinstance(requirements[0], RequirementsPackageEntry)


def test_parse_requirements_ignores_leading_and_trailing_whitespace():
    lines = [
        "   django==1.0   ",
        "  -r    ./otherfile.txt  ",
        " -e ../",
        "    git+https://github.com/test/test#tag",
    ]

    requirements = list(parse_requirements_list(source, lines))
    assert len(requirements) == 4

    assert isinstance(requirements[2], RequirementsEditableEntry)
    assert isinstance(requirements[3], RequirementsVCSPackageEntry)

    assert isinstance(requirements[0], RequirementsPackageEntry)
    assert requirements[0].source.path == source.path
    assert requirements[0].source.line == "django==1.0"
    assert requirements[0].source.line_number == 1
    assert requirements[0].name == "django"
    assert requirements[0].version == "1.0"
    assert requirements[0].operator == "=="

    assert isinstance(requirements[1], RequirementsRecursiveEntry)
    assert requirements[1].source.path == source.path
    assert requirements[1].source.line == "-r ./otherfile.txt"
    assert requirements[1].source.line_number == 2
    assert requirements[1].absolute_path == os.path.join(
        os.getcwd(), "otherfile.txt"
    )

    assert isinstance(requirements[2], RequirementsEditableEntry)
    assert requirements[2].source.path == source.path
    assert requirements[2].source.line == "-e ../"
    assert requirements[2].source.line_number == 3
    assert requirements[2].absolute_path == os.path.realpath(
        os.path.join(os.getcwd(), "..")
    )

    assert isinstance(requirements[3], RequirementsVCSPackageEntry)
    assert requirements[3].source.path == source.path
    assert requirements[3].source.line == "git+https://github.com/test/test#tag"
    assert requirements[3].source.line_number == 4
    assert requirements[3].vcs == "git"
    assert requirements[3].uri == "https://github.com/test/test"
    assert requirements[3].tag == "tag"
