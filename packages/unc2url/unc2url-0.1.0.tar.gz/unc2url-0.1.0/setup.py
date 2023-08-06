"""A UNC to URL Converter."""

import os

from setuptools import find_packages, setup  # type: ignore


def package_files(directory):
    """Automatically add data resources."""
    paths = []
    # pylint: disable=unused-variable
    for (path, _directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append((directory, [os.path.join(path, filename)]))
    return paths


APP = ["unc2url"]
APP_NAME = "UNC to URL"
AUTHOR = "Alexander Willner"
AUTHOR_MAIL = "alex@willner.ws"
DESCRIPTON = "A UNC to URL Converter."
URL = "https://github.com/alexanderwillner/unc2url"
DATA_FILES = package_files("")
OPTIONS = {
    "argv_emulation": False,
}


with open("README.md", "r") as fh:
    LONG_DESRIPTION = fh.read()

setup(
    app=APP,
    author=AUTHOR,
    author_email=AUTHOR_MAIL,
    name="unc2url",
    description=DESCRIPTON,
    long_description=LONG_DESRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Natural Language :: English",
    ],
    python_requires=">=3.6",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
    entry_points={
        "console_scripts": [
            "unc2url = unc2url.unc2url:main",
        ]
    },
    install_requires=[],
)
