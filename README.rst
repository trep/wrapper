
===============
OpenTrepWrapper
===============

Import the module::

    >>> from OpenTrepWrapper import *


This module is an OpenTrep binding::

    >>> otp = OpenTrepLib(DEFAULT_DB, DEFAULT_LOG)
    >>> otp.search('sna francsico los angeles', DEFAULT_FMT)
    ([(3.93..., 'SFO'), (46.28..., 'LAX')], '')

