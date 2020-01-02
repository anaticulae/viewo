#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import glob
import itertools
import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
UTF8 = 'utf8'

with open(os.path.join(ROOT, 'README.md'), mode='rt', encoding=UTF8) as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'viewo/__init__.py'), mode='rt', encoding=UTF8) as fp: # yapf:disable
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), mode='rt', encoding=UTF8) as fp: # yapf:disable
    INSTALL_REQUIRES = [
        line for line in fp.readlines() if line and '#' not in line
    ]


def datafiles():
    files = glob.glob('viewo/**/**.*', recursive=True)
    collected = [
        item for item in files
        if not any([item.endswith(ext) for ext in ['py', 'pyc']])
    ]
    grouped = itertools.groupby(collected, key=lambda x: os.path.split(x)[0])
    result = [(item[0], list(item[1])) for item in grouped]

    result += ('.', [
        'CHANGELOG.md',
        'README.md',
        'requirements.txt',
    ]),
    return result


if __name__ == "__main__":
    # allow setup.py to run from another directory
    os.chdir(ROOT)
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        data_files=datafiles(),
        description='Let\'s make some flask',
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        long_description=README,
        name='viewo',
        platforms='any',
        url='https://dev.package.checkitweg.de/viewo',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'viewo',
            'viewo.waiting',
        ],
    )
