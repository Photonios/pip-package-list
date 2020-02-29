import os

from typing import Generator

import setuptools

from .requirements import (
    RequirementsEntry,
    RequirementsEntrySource,
    parse_requirements,
)


def parse_setup_py(file_path: str) -> Generator[RequirementsEntry, None, None]:
    setup_kwargs = {}

    def _setup_proxy(*args, **kwargs):
        setup_kwargs.update(dict(kwargs))

    setuptools.setup = _setup_proxy

    with open(file_path, "r") as fp:
        exec(fp.read())

    source = RequirementsEntrySource(
        path=os.path.realpath(file_path), line=None, line_number=None
    )

    requirements = setup_kwargs.get("install_requires") or []

    extras_require = setup_kwargs.get("extras_require") or {}
    for _, extra_requirements in extras_require.items():
        requirements.extend(extra_requirements)

    for requirement in parse_requirements(source, requirements):
        yield requirement
