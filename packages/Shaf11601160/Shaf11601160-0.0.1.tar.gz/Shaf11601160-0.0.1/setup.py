import setuptools
from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Shaf11601160",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A big example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	data_files = [ ('', ['AliShafieiShel/file6.txt']) ],
	package_data={
        '': ['*.txt'],
        'AliShafieiShel': ['*.txt'],
    },
)