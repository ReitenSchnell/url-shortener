#!/usr/bin/python
#
# setup.py - standard Python build-and-package program

from setuptools import find_packages, setup


def read_requirements(filename):
    with open(filename) as f:
        return [req for req in (req.partition("#")[0].strip() for req in f) if req]


setup(
    name="shortener-api",
    version="0.1.0",
    description="RESTful web service for url shortening",
    author="",
    author_email="",
    packages=find_packages("."),
    install_requires=read_requirements('requirements.txt'),
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": [
           "shortener-api = shortener_api.__main__:main"
        ]
    }
)
