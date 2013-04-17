===============
OpenTrepWrapper
===============

This module does not install OpenTrep, you have to do that.

Import the module::

 >>> from OpenTrepWrapper import OpenTrepLib

This module is an OpenTrep binding::

 >>> with OpenTrepLib() as otp:
 ...     otp.search('sna francsico los angeles')
 ([(0.039..., 'SFO'), (0.462..., 'LAX')], '')

You may put the package created by setuptools in the repository with::

 % rake
