import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="harshit",
    version="0.0.1",
    description="It squares the number",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/shadow-python/pip-package",
    author="Harshit Mehra",
    author_email="harshitmeh111@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3" ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
