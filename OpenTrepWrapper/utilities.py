# -*- coding: utf-8 -*-
#
# Source: https://github.com/trep/wrapper/tree/master/OpenTrepWrapper/utilities.py
#
# Authors: Alex Prengere, Denis Arnaud
#

import json
import os
import errno

# Default settings
DEFAULT_POR = '/tmp/opentraveldata/optd_por_public_all.csv'
DEFAULT_IDX = '/tmp/opentrep/xapian_traveldb'
DEFAULT_FMT = 'S'
DEFAULT_LOG = '/tmp/opentrep/opentrepwrapper.log'


def _test():
    '''
    Launching doctests.
    '''
    import doctest

    opt = doctest.ELLIPSIS

    doctest.testmod(optionflags=opt)


