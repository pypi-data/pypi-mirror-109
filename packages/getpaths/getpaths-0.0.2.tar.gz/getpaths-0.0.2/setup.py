from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Pathing Library'


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


# Setting up
setup(
        name="getpaths", 
        version=VERSION,
        author="Jv Kyle Eclarin",
        author_email="<jvykleeclarin@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'pathing', 'path'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)