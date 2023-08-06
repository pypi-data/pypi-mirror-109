from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Pathing Library'
LONG_DESCRIPTION = 'Pathing made easier. Inspired by pathlib'

# Setting up
setup(
        name="getpaths", 
        version=VERSION,
        author="Jv Kyle Eclarin",
        author_email="<jvykleeclarin@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
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