import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent


README = (HERE / "README.md").read_text()


setup(
    name="craxkhash",
    version="1.0.0",
    description="Craxk is a UNIQUE AND NON-REPLICABLE Hash that uses data from the hardware where it is executed to form a hash that can only be reproduced by a single machine.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ZaikoARG/Craxk",
    author="ZaikoARG",
    author_email="zaikoarg@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[""],
    include_package_data=True
)