######################################################################
#
# File: setup.py
#
# Copyright 2019 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import sys

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, __version__ as setuptoolsversion
# To use a consistent encoding
from codecs import open
from os import path

#require at least setuptools 20.2 for PEP 508 conditional dependency support
MIN_SETUPTOOLS_VERSION = (20, 2)
if tuple(int(x) for x in setuptoolsversion.split('.')[:2]) < MIN_SETUPTOOLS_VERSION:
    sys.exit(
        'setuptools %s.%s or later is required. To fix, try running: pip install "setuptools>=%s.%s"'
        % (MIN_SETUPTOOLS_VERSION * 2)
    )

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

with open('requirements-test.txt', encoding='utf-8') as f:
    requirements_test = f.read().splitlines()

with open('requirements-setup.txt', encoding='utf-8') as f:
    requirements_setup = f.read().splitlines()

with open('requirements-doc.txt', encoding='utf-8') as f:
    requirements_doc = f.read().splitlines()

version = __import__('b2sdk').__version__

setup(
    name='b2sdk',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,
    description='Backblaze B2 SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://github.com/Backblaze/b2-sdk-python',

    # Author details
    author='Backblaze, Inc.',
    author_email='support@backblaze.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        # ??? What are the right classifiers for a command-line tool? ???
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='backblaze b2 cloud storage',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'test']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requirements,

    # requirements for tests
    tests_require=requirements_test,

    # putting nose in test_requires caused a chicken/egg problem
    # but apparently setup_requires is broken on most python versions
    # setup_requires=requirements_setup,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'doc': requirements_doc,
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'b2sdk':
            [
                'requirements.txt',
                'requirements-test.txt',
                'requirements-setup.txt',
                'requirements-doc.txt',
            ]
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[
        #('my_data', ['data/data_file'])
    ],
)
