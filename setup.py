#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 14:45:57 2019

@author: malkusch
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qSMLM",
    version="19.01",
    author="Sebastian Malkusch",
    author_email="malkusch@chemie.uni-frankfurt.de",
    description="A package for modeling single-molecule localization-microscopy blinking kinetics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SMLMS/qSMLM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL3 License",
        "Operating System :: OS Independent",
    ],
)
