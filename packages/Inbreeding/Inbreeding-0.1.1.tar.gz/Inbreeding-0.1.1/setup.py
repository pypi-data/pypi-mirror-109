#!/usr/bin/env python3

import setuptools

"""
This file is necessary to allow building software using the following command:
python3 -m build
The consecutive installation can be conducted using pip3 install dists/file.whl
Best ressource regarding the documentation:
https://stackoverflow.com/questions/64150719/how-to-write-a-minimally-working-pyproject-toml-file-that-can-install-packages/64151860#64151860
"""

setuptools.setup()