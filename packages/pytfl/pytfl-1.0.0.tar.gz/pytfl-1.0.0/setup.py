import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "readme.md").read_text()

# This call to setup() does all the work
setup(
    name="pytfl",
    version="1.0.0",
    description="Team Formation Library with Tensorflow Machine Learning",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/radinhamidi/Team_Formation_Library/",
    author="Radin Hamidi, Aabid Mitha",
    author_email="radin@ryerson.ca",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["teamFormationLibrary"],
    include_package_data=True,
    install_requires=["tensorflow", "keras", "gensim", "nltk", "scikit-learn", "sklearn"]
)
