# pip-package-list

[![License](https://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
[![PyPi](https://badge.fury.io/py/pip-package-list.svg)](https://pypi.python.org/pypi/pip-package-list)
![test](https://github.com/Photonios/pip-package-list/workflows/test/badge.svg)

A small and definitely faulty tool that tries to form a list of packages that you depend on. This is useful in mono-repo's where all dependencies are split into dozens of `requirements.txt` and `setup.py` files.

One particular use-case that fueled the development of this tool was to create a flat list of dependencies to pre-install in a Docker base image.

Although there is a number of tools that parse and resolve requirement files, I did not find any that parse `setup.py` files and extract `install_requires`.

## Usage

    usage: pip-package-list [-h] [--recurse-recursive] [--recurse-editable]
                            [--inline-constraints] [--dedupe] [--remove-editable]
                            [--remove-recursive] [--remove-constraints]
                            [--remove-vcs] [--remove-wheel] [--remove-unversioned]
                            [--remove-index-urls]
                            file_paths [file_paths ...]

    positional arguments:
      file_paths            list of requirements.txt or setup.py files

    optional arguments:
      -h, --help            show this help message and exit
      --recurse-recursive   recurse into -r entries
      --recurse-editable    recurse into -e entries
      --inline-constraints  recurse into -c entries and inline them
      --dedupe              de-duplicate the resulting list
      --remove-editable     remove editable requirements from the final list
      --remove-recursive    remove recursive requirements (-r) from the final list
      --remove-constraints  remove constraints (-c) from the final list
      --remove-vcs          remove vcs requirements from the final list
      --remove-wheel        remove wheel requirements from the final list
      --remove-unversioned  remove requirements without a version number from the
                            final list
      --remove-index-urls   remove -i entries (index urls) from the final list
