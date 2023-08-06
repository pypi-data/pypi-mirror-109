import setuptools
import io
from io import open
from setuptools import setup

with open("README.md", encoding='utf-8') as f:
    long_description = f.read()

    version = '0.0.1'

long_description = 'Python module for building a tree structure of a file path'

setup(
    name = 'f_path_tree',
    version = version,
    author = 'VadimTarasov132',
    author_email = 'tarasov.2120@mail.ru',
    description=(
        u'Python module for building a tree structure of a file path'
        u'File path tree'
    ),
    long_description = long_description,
    url = 'https://github.com/vadim-tarasov/f-path-tree',
    download_url = 'https://github.com/vadim-tarasov/f-path-tree/archive/refs/heads/master.zip'.format(
        version
    ),
    packages = ['f_path_tree'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
    ]
)
