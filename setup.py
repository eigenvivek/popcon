import os
import sys
from setuptools import setup, find_packages

PACKAGE_NAME = "popcon"
DESCRIPTION = "Population-level connectome analysis in Python!"
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()
AUTHOR = ("Vivek Gopalakrishnan",)
AUTHOR_EMAIL = "vgopala4@jhu.edu"
URL = "https://github.com/v715/popcon"
MINIMUM_PYTHON_VERSION = 3, 5
REQUIRED_PACKAGES = [
    "graspy>=0.1",
    "mgc>=0.0.1",
    "numpy>=1.18",
    "pandas>=0.25.0",
    "statsmodels>=0.10.0",
    "tqdm>=4.41.0",
]

# Find popcorn's version
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
for line in open(os.path.join(PROJECT_PATH, "popcon", "__init__.py")):
    if line.startswith("__version__ = "):
        VERSION = line.strip().split()[2][1:-1]


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


check_python_version()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=REQUIRED_PACKAGES,
    url=URL,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    test_suite="tests",
)
