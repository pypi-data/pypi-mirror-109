import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="opu",
    version="0.0.1",
    description="Utilities for quick automation",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Oskar Person",
    author_email="",
    license="AGPL v3.0",
    packages=setuptools.find_packages(exclude=['tests']),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    url="https://github.com/positivedefinite/op",
    zip_safe=False,
)