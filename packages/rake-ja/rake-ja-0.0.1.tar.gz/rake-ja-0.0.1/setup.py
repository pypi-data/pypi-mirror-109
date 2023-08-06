from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name="rake-ja",
    version="0.0.1",
    description="A Japanese Keyword Extraction Library",
    long_description="A Japanese Keyword Extraction Library based on rake/nltk",
    license="MIT",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=[
        "mecab-python3>=0.7",
        "rake-nltk>=1.0.4",
        "unidic-lite~=1.0.8"
    ],
    dependency_links=[],
    python_requires='>=3.6',
)
