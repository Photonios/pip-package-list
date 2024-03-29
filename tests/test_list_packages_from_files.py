import os

from pippackagelist.list_packages_from_files import list_packages_from_files

test_case_1_path = os.path.join(
    os.path.dirname(__file__), "./test-cases/list-1"
)


def test_list_packages_from_files_from_requirements():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement) for requirement in list_packages_from_files([path])
    ]
    assert raw_requirements == [
        "-e tests/test-cases/list-1/package-1[local,special]",
        "django==1.1",
        "redis==2.0",
        "-r tests/test-cases/list-1/requirements-nested.txt",
        "-i https://mypackages.com/repo",
        "mypackage==4.2.1",
        "-c tests/test-cases/list-1/constraints.txt",
    ]


def test_list_packages_from_files_from_requirements_recurse_recursive():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement)
        for requirement in list_packages_from_files(
            [path], recurse_recursive=True
        )
    ]

    assert raw_requirements == [
        "-e tests/test-cases/list-1/package-1[local,special]",
        "django==1.1",
        "redis==2.0",
        "-i https://mypackages.com/repo",
        "mypackage==4.2.1",
        "-c tests/test-cases/list-1/constraints.txt",
        "test>=1.2",
        "-e tests/test-cases/list-1/package-2",
    ]


def test_list_packages_from_files_from_requirements_recurse_editable():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement)
        for requirement in list_packages_from_files(
            [path], recurse_editable=True
        )
    ]

    assert raw_requirements == [
        "django==1.1",
        "redis==2.0",
        "-r tests/test-cases/list-1/requirements-nested.txt",
        "-i https://mypackages.com/repo",
        "mypackage==4.2.1",
        "-c tests/test-cases/list-1/constraints.txt",
        "pyyaml>=2.1",
        "grpcio==9.1",
        "mypackage",
        "specialpackage",
    ]


def test_list_packages_from_files_from_requirements_inline_constraints():
    path = os.path.join(test_case_1_path, "requirements.txt")

    raw_requirements = [
        str(requirement)
        for requirement in list_packages_from_files(
            [path], inline_constraints=True
        )
    ]
    assert raw_requirements == [
        "-e tests/test-cases/list-1/package-1[local,special]",
        'https://myindex.com/pypi/django-2.0-macos.whl#egg=django ; sys_platform == "darwin"',
        'https://myindex.com/pypi/django-2.0-linux.whl#egg=django ; sys_platform == "linux"',
        "redis==2.0",
        "-r tests/test-cases/list-1/requirements-nested.txt",
        "-i https://mypackages.com/repo",
        "mypackage==4.2.1",
    ]
