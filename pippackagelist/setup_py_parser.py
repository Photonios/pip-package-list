import os
import setuptools

from typing import Generator

from .requirements import RequirementsEntry, RequirementsEntrySource, parse_requirements


def parse_setup_py(file_path: str) -> Generator[RequirementsEntry, None, None]:
    setup_kwargs = {}

    def _setup_proxy(*args, **kwargs):
        setup_kwargs.update(dict(kwargs))
    setuptools.setup = _setup_proxy

    path = os.path.join(file_path, "setup.py")
    with open(path, "r") as fp:
        exec(fp.read())

    source = RequirementsEntrySource(
        path=path,
        line=None,
        line_number=None,
    )

    requirements = setup_kwargs.get("install_requires") or []
    for requirement in parse_requirements(source, requirements):
        yield requirement
