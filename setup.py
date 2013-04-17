#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Main installation script.
'''

from setuptools import setup

setup(
    name = 'OpenTrepWrapper',
    version = '0.7',
    author = 'Alex Prengere',
    author_email = 'alex.prengere@gmail.com',
    url = 'https://github.com/trep/wrapper',
    description = 'A Python wrapper module for OpenTrep.',
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
        #Public
        #'simplejson', # --> json now
    ],
)
