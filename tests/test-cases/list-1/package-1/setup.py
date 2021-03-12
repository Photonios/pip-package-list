from setuptools import setup

setup(
    name="package-1",
    install_requires=["pyyaml>=2.1", "grpcio==9.1",],
    extras_require={
        "test": ["pytest==5.2"],
        "local": ["mypackage"],
        "special": ["specialpackage"],
    },
)
