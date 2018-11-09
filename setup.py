#!/usr/bin/env python3

import sys
from setuptools import setup
from setuptools import find_packages


setup(
    name="highfinesse-net",
    version="0.1",
    description="Driver for HighFinesse Wavement used in opticlock",
    long_description=open("README.rst").read(),
    author="Robert Jördens",
    author_email="rj@quartiq.de",
    url="https://github.com/quartiq/highfinesse-net",
    download_url="https://github.com/quartiq/highfinesse-net",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "aqctl_highfinesse_net = highfinesse_net.aqctl_highfinesse_net:main",
        ],
    },
    test_suite="highfinesse_net.test",
    license="LGPLv3+",
)
