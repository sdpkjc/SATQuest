#!/usr/bin/env python
# setup.py
from setuptools import find_packages, setup

setup(
    name="satquest",
    version="0.1.0",
    author="Yanxiao Zhao",
    author_email="pazyx728@gmail.com",
    description="SATQuest",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sdpkjc/SATQuest",
    packages=find_packages("."),
    python_requires=">=3.9",
    install_requires=[
        "python-sat==1.8.dev14",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
