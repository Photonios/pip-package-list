import os

from pippackagelist.list import list as list_packages

test_case_1_path = os.path.join(
    os.path.dirname(__file__), "./fixtures/list-test-case-1"
)


def test_list_from_requirements():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement) for requirement in list_packages([path])
    ]
    assert raw_requirements == [
        "-e tests/fixtures/list-test-case-1/package-1",
        "django==1.1",
        "redis==2.0",
        "-r tests/fixtures/list-test-case-1/requirements-nested.txt",
    ]


def test_list_from_requirements_recurse_recursive():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement)
        for requirement in list_packages([path], recurse_recursive=True)
    ]

    assert raw_requirements == [
        "-e tests/fixtures/list-test-case-1/package-1",
        "django==1.1",
        "redis==2.0",
        "test>=1.2",
        "-e tests/fixtures/list-test-case-1/package-2",
    ]


def test_list_from_requirements_recurse_editable():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement)
        for requirement in list_packages([path], recurse_editable=True)
    ]

    assert raw_requirements == [
        "django==1.1",
        "redis==2.0",
        "-r tests/fixtures/list-test-case-1/requirements-nested.txt",
        "pyyaml>=2.1",
        "grpcio==9.1",
        "pytest==5.2",
    ]
