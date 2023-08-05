#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re
import glob


from setuptools import setup, find_packages
from setuptools.extension import Extension

try:
    from Cython.Distutils import build_ext as _build_ext
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    from setuptools.command.build_ext import build_ext as _build_ext
    HAVE_CYTHON = False

classifiers = """\
    Development Status :: 4 - Beta
    Operating System :: OS Independent
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.4
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
"""


def _read(*parts, **kwargs):
    filepath = os.path.join(os.path.dirname(__file__), *parts)
    encoding = kwargs.pop('encoding', 'utf-8')
    with io.open(filepath, encoding=encoding) as fh:
        text = fh.read()
    return text

def get_version():
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        _read('pairtools', '__init__.py'),
        re.MULTILINE).group(1)
    return version

long_description = _read('README.md')

install_requires = [l for l in _read('requirements.txt').split('\n') if l]

def get_ext_modules():
    ext = '.pyx' if HAVE_CYTHON else '.c'
    src_files = glob.glob(os.path.join(
        os.path.dirname(__file__),
        "pairtools", "*" + ext))

    ext_modules = []
    for src_file in src_files:
        name = "pairtools." + os.path.splitext(os.path.basename(src_file))[0]
        ext_modules.append(Extension(name, [src_file]))

    if HAVE_CYTHON:
        # .pyx to .c
        ext_modules = cythonize(ext_modules)  #, annotate=True

    return ext_modules


class build_ext(_build_ext):
    # Extension module build configuration
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Fix to work with bootstrapped numpy installation
        # http://stackoverflow.com/a/21621689/579416
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


    def run(self):

        # Import numpy here, only when headers are needed
        import numpy

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

        # Call original build_ext command
        _build_ext.run(self)



setup(
    name='pairtools',
    author='Mirny Lab',
    author_email='espresso@mit.edu',
    version=get_version(),
    license='MIT',
    description='CLI tools to process mapped Hi-C data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['genomics', 'bioinformatics', 'Hi-C', 'contact'],
    url='https://github.com/mirnylab/pairtools',
    ext_modules=get_ext_modules(),
    cmdclass = {'build_ext': build_ext},
    zip_safe=False,
    classifiers=[s.strip() for s in classifiers.split('\n') if s],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
             'pairtools = pairtools:cli',
             #'pairsamtools = pairtools:cli',
        ]
    },
    packages = find_packages()
)
