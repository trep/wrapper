#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Main installation script.
'''

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'OpenTrepWrapper',
    version = '0.7.5.post1',
    author = 'Alex Prengere',
    author_email = 'alex.prengere@gmail.com',
    url = 'https://github.com/trep/wrapper',
    description = 'A Python wrapper module for OpenTrep',
    long_description = read('README.md'),
    long_description_content_type = 'text/markdown',
    entry_points = {
        'console_scripts' : [
            'OpenTrep = OpenTrepWrapperMain:main',
        ]
    },
    py_modules = [
        'OpenTrepWrapper',
        'OpenTrepWrapperMain'
    ],
    install_requires = [
    ],
    #sanitize_lib = ['-lasan'] if cc == 'gcc' and not is_macos else [],
)

