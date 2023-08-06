import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="lucid-data",
    version="0.1.0",
    description="Scripts for processing, profiling, and publishing data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/liquidcarbon/lucid",
    author="Alex Kislukhin",
    author_email="liquidc@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=["lucid"],
    include_package_data=True,
    install_requires=[
        "bokeh",
        "boto3",
        "pandas",
    ],
    python_requires=">=3.7",
)
