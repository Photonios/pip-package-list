# pip-package-list

[![License](https://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
[![PyPi](https://badge.fury.io/py/pip-package-list.svg)](https://pypi.python.org/pypi/pip-package-list)
![test](https://github.com/Photonios/pip-package-list/workflows/test/badge.svg)

A small and definitely faulty tool that tries to form a list of packages that you depend on. This is useful in mono-repo's where all dependencies are split into dozens of `requirements.txt` and `setup.py` files.

One particular use-case that fueled the development of this tool was to create a flat list of dependencies to pre-install in a Docker base image.

Although there is a number of tools that parse and resolve requirement files, I did not find any that parse `setup.py` files and extract `install_requires`.

## Usage

    pip-package-list [requirements.txt or setup.py file...]

You can specify one or more `requirements.txt` or `setup.py` files to be parsed and resolved.
