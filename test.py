#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import doctest

import OpenTrepWrapper


def main():

    opt = doctest.ELLIPSIS

    s = unittest.TestSuite()

    s.addTests(doctest.DocTestSuite(OpenTrepWrapper, optionflags=opt))
    s.addTests(doctest.DocFileSuite('README.md', optionflags=opt))

    return s


if __name__ == '__main__':

    unittest.main(defaultTest='main')

