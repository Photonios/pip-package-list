from setuptools import setup

setup(
    name="mywhopackage",
    install_requires=["django==1.0", ],
    extras_require={"test": ["pytest==2.0", ], "docs": ["Sphinx==1.0", ], },
)
