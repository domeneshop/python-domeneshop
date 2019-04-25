import os
import sys

from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.insert(0, SRC_DIR)

from domeneshop import __version__  # pylint: disable=wrong-import-position

INSTALL_REQUIRES = ["requests>=2.21.0"]

DEV_EXTRAS = ["black", "mypy", "prospector", "wheel"]

with open("README.rst", "rb") as f:
    LONG_DESCRIPTION = f.read().decode("utf-8")

setup(
    name="domeneshop",
    version=__version__,
    description="Domeneshop API library",
    author="Domeneshop AS",
    url="https://github.com/domeneshop/python-domeneshop",
    license="MIT License",
    long_description=LONG_DESCRIPTION,
    python_requires="!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    author_email="kundeservice@domeneshop.no",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require={"dev": DEV_EXTRAS},
)
