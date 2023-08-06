# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:07:52 2019

@author: Innotechway
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Phygital-pkg",
    version="0.0.1",
    author="Renuka Angole",
    author_email="renuka.angole@gmail.com",
    description="A powerful package to work on IoT projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)