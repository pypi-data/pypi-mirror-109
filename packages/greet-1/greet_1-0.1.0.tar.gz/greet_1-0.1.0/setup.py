# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file


# This call to setup() does all the work
setup(
    name="greet_1",
    version="0.1.0",
    description="Demo library for testing",
    long_description="Long txt",
    long_description_content_type="text/markdown",
    url="https://www.google.com/",
    author="Devil 101",
    author_email="lucifer@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["greet_1"],
    include_package_data=True,
 
)
