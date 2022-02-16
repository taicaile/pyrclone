"""setup"""
import io

from setuptools import find_packages, setup


def read_file(filename):
    """read file content"""
    with io.open(filename, encoding="utf-8") as fp:
        return fp.read().strip()


def read_requirements(filename):
    """read requirements"""
    return [
        line.strip()
        for line in read_file(filename).splitlines()
        if not line.startswith("#")
    ]


setup(
    name="pyrclone",
    version="0.2.1",
    description="Python wrapper for Rclone",
    long_description=read_file("README.md"),
    author="taicaile",
    url="https://github.com/taicaile/pyrclone",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
)
