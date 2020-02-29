from setuptools import setup

setup(
    name="mywhopackage",
    install_requires=["django==1.0", "cookie>=1.2", "-r ../test.txt", "-e ..",],
)
