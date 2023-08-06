#!/usr/bin/env python
# import sys
# # Test Python's version
# major, minor = sys.version_info[0:2]
# if (major, minor) == (3, 9):
#     sys.stderr.write('\nPython 3.9 is not supported by numba at this time.\n')
#     sys.exit(1)
from setuptools import find_packages, setup
from distutils.command.sdist import sdist
cmdclass={'sdist': sdist}

def readme():
    with open('README.rst', encoding='utf-8', mode='r') as f:
        return f.read()

setup(name='mpi4py_utilities',
    packages=find_packages(),
    scripts=[],
    version="1.0.2",
    description='Utility functions for mpi4py',
    long_description=readme(),
    url='https://github.com/leonfoks/mpi4py_utilities/archive/refs/tags/1.0.1.tar.gz',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    author='Leon Foks',
    author_email='leonfoks@gmail.com',
    install_requires=[
        'numpy',
        'sphinx',
    ],
)

