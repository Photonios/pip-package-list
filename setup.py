import distutils.cmd
import os
import subprocess

from setuptools import find_packages, setup


class BaseCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def create_command(text, commands):
    """Creates a custom setup.py command."""

    class CustomCommand(BaseCommand):
        description = text

        def run(self):
            for cmd in commands:
                subprocess.check_call(cmd)

    return CustomCommand


with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read()


setup(
    name="pip-package-list",
    version="0.0.7",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="Generate a flat list of packages Pip would install.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Photonios/pip-package-list",
    author="Swen Kooij",
    author_email="swenkooij@gmail.com",
    keywords=["pip", "package", "resolver", "list", "requirements"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ],
    entry_points={
        "console_scripts": ["pip-package-list=pippackagelist.__main__:main"]
    },
    python_requires=">=3.7",
    install_requires=["setuptools"],
    extras_require={
        "test": ["pytest==5.2.2", "pytest-cov==2.8.1",],
        "analysis": [
            "black==19.10b0",
            "flake8==3.7.7",
            "autoflake==1.3",
            "autopep8==1.4.4",
            "isort==4.3.20",
            "docformatter==1.3.1",
        ],
    },
    cmdclass={
        "lint": create_command(
            "Lints the code",
            [["flake8", "setup.py", "pippackagelist", "tests"]],
        ),
        "lint_fix": create_command(
            "Lints the code",
            [
                [
                    "autoflake",
                    "--remove-all-unused-imports",
                    "-i",
                    "-r",
                    "setup.py",
                    "pippackagelist",
                    "tests",
                ],
                ["autopep8", "-i", "-r", "setup.py", "pippackagelist", "tests"],
            ],
        ),
        "format": create_command(
            "Formats the code",
            [["black", "setup.py", "pippackagelist", "tests"]],
        ),
        "format_verify": create_command(
            "Checks if the code is auto-formatted",
            [["black", "--check", "setup.py", "pippackagelist", "tests"]],
        ),
        "format_docstrings": create_command(
            "Auto-formats doc strings", [["docformatter", "-r", "-i", "."]]
        ),
        "format_docstrings_verify": create_command(
            "Verifies that doc strings are properly formatted",
            [["docformatter", "-r", "-c", "."]],
        ),
        "sort_imports": create_command(
            "Automatically sorts imports",
            [
                ["isort", "setup.py"],
                ["isort", "-rc", "pippackagelist"],
                ["isort", "-rc", "tests"],
            ],
        ),
        "sort_imports_verify": create_command(
            "Verifies all imports are properly sorted.",
            [
                ["isort", "-c", "setup.py"],
                ["isort", "-c", "-rc", "pippackagelist"],
                ["isort", "-c", "-rc", "tests"],
            ],
        ),
        "fix": create_command(
            "Automatically format code and fix linting errors",
            [
                ["python", "setup.py", "format"],
                ["python", "setup.py", "format_docstrings"],
                ["python", "setup.py", "sort_imports"],
                ["python", "setup.py", "lint_fix"],
                ["python", "setup.py", "lint"],
            ],
        ),
        "verify": create_command(
            "Verifies whether the code is auto-formatted and has no linting errors",
            [
                ["python", "setup.py", "format_verify"],
                ["python", "setup.py", "format_docstrings_verify"],
                ["python", "setup.py", "sort_imports_verify"],
                ["python", "setup.py", "lint"],
            ],
        ),
        "test": create_command(
            "Runs all the tests",
            [
                [
                    "pytest",
                    "--cov=pippackagelist",
                    "--cov-report=term",
                    "--cov-report=xml:reports/xml",
                    "--cov-report=html:reports/html",
                    "--junitxml=reports/junit/tests.xml",
                ]
            ],
        ),
    },
)
