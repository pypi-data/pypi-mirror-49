"""
Code 2 JSON: A tool to easily and automatically write all your source code to a JSON file and the other way around

https://gitlab.com/Deathray_II/code2json
"""

from os import path
from setuptools import setup, find_packages
from src.code2json.cmd.cmd import VERSION

with open("README.md", "r") as fh:
    readme_description = fh.read()

setup(
    name="code2json",
    version=VERSION,
    description="A tool to easily automatically write all your source code to a JSON file and the other way around",
    long_description=readme_description,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='Apache-2.0',
    author='Jasper Steegmans',
    author_email='jasper.steegmans.code@gmail.com',
    url='https://gitlab.com/Deathray_II/code2json',
    entry_points={
        'console_scripts': [
            'code2json=code2json.cmd.cmd:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
