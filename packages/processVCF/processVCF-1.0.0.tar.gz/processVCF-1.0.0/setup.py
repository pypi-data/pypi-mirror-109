#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Import the needed setuptools 
import setuptools

# Read in the ReadMe and license files 
with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open('LICENSE', "r", encoding="utf-8") as license_file:
    license = license_file.read()


# Required Packages 
requirements = [
    'pandas'
]


setuptools.setup(
    name="processVCF",
    version="1.0.0",
    author="Maxwell Brown",
    author_email="mbrown@broadinstitute.org",
    description="Package to parse VCF files.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license=license,
    url="https://github.com/brownmp/processVCF",
    classifiers=([
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Natural Language :: English'
    ]),
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)


