#!/usr/bin/env python

# https://packaging.python.org/tutorials/packaging-projects
# docker run -it  -v $PWD:/app  -w /app python:3.8  bash
# python3 -m pip install --user --upgrade twine
# python3 setup.py sdist clean
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --skip-existing --verbose dist/*

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pbrats", 
    version="0.11.1",
    author="xrgopher",
    author_email='xrgopher@outlook.com',
    url='https://gitlab.com/xrgopher/pbrats',
    description="Power Bridge Record artistic table system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include=['pbr','*']),
    package_data={'pbr': ['result.xlsx', 'result.html']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'pbr=pbr.pbr:main',
            'pbr_tables=pbr.pbr_tables:main',
            'pbr_gen=pbr.pbr_gen:main'
        ],
    },
    install_requires=[
        'repackage',
        'bridge_utils',
        'pandas',
        'openpyxl',
        'xlsxwriter'
    ],
    python_requires='>=3.6',
)
