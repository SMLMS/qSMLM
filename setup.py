# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 15:19:22 2019

@author: malkusch
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qSMLM",
    version="19.01",
    author="Sebastian Malkusch",
    author_email="malkusch@chemie.uni-frankfurt.com",
    description="a package for modeling single molecule localization microscopy blinking kinetics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SMLMS/qSMLM",
    packages=setuptools.find_packages(),
	install_requires=['numpy',
						'matplotlib',
						'scipy',
						'IPython',
						'ipywidgets'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
)