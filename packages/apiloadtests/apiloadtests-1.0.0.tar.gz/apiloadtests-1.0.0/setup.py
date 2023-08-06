"""Setup script for apiloadtests"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="apiloadtests",
    version="1.0.0",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/aqua-regia/apiloadtests",
    author="Syed Hassan Ashraf",
    author_email="hassanashraf8888@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    packages=find_packages(exclude=("tests",)),
    # entry_points={"console_scripts": ["apiloadtests.__main__:main"]},
)
