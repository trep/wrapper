OpenTrepWrapper
===============

This module does not install OpenTrep, you have to do that.

Import the module:
```python

 >>> from OpenTrepWrapper import OpenTrepLib

```

This module is an OpenTrep binding:
```python

 >>> with OpenTrepLib() as otp:
 ...     otp.search('sna francsico los angeles')
 ([(0.039..., 'SFO'), (0.462..., 'LAX')], '')

```

You may put the package created by `setuptools` in the repository with:
```bash
$ export TREP_VER="0.07.3"
$ export TREP_DIR="$HOME/dev/deliveries/opentrep-$TREP_VER"
$ export PYTHONPATH=$TREP_DIR/lib/python3.7/site-packages/pyopentrep:$TREP_DIR/lib
$ rake
```


