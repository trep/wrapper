#!/usr/bin/python
# -*- coding: utf-8 -*-


from setuptools import setup

setup(
    name = 'OpenTrepWrapper',
    version = '0.3',
    author = 'Alex Prengere',
    author_email = 'alex.prengere@amadeus.com',
    url = "http://gitorious.orinet.nce.amadeus.net/ipt/opentrepwrapper",
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
    #dependency_links = [
    #    'http://orinet/pythonpackages'
    #],
    install_requires = [
        #Public
        'simplejson',
    ],
)
