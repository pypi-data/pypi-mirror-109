"""Setup script for realpython-reader"""
import os.path
from setuptools import setup
# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))
# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()
# This call to setup() does all the work
setup(
    name="gr_currency",
    version="0.0.1",
    description="Real Time currency converter, Internet connection required",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/greatRaksin/gr_currency",
    author="Great Raksin",
    author_email="greatRaksin@icloud.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["converter"],
    include_package_data=True,
    install_requires=[
        "requests",
    ],
)