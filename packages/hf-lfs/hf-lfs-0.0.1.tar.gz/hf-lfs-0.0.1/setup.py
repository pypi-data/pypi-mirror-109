import os
from setuptools import setup, find_packages
from fetch_lfs import fetch

fetch()

setup(
    name = "hf-lfs",
    version = "0.0.1",
    author = "Lysandre Debut",
    author_email = "lysandre@huggingface.co",
    license = "MIT",
    keywords = "git lfs huggingface hf",
    packages=find_packages("src"),
    package_dir={"lfs": "src/lfs"},
    package_data={"lfs": ["**"]},
    entry_points={"console_scripts": ["git-lfs=lfs:main"]},
    url = "http://huggingface.co",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
