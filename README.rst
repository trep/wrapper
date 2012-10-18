
===============
OpenTrepWrapper
===============

This module does not install OpenTrep, you have to do that.

Import the module::

    >>> from OpenTrepWrapper import *

This module is an OpenTrep binding::

    >>> with OpenTrepLib(DEFAULT_DB, DEFAULT_LOG) as otp:
    ...     otp.search('sna francsico los angeles', DEFAULT_FMT)
    ([(3.93..., 'SFO'), (46.28..., 'LAX')], '')

You may put the package created by setuptools in the repository with::

    % scp dist/OpenTrepWrapper-*.tar.gz ori-data@nceorilnx04:/remote/oridata/www/pythonpackages

