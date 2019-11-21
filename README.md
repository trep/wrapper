OpenTrepWrapper
===============

# Refefences
* OpenTREP project: https://github.com/trep/opentrep
* This GitHub project: https://github.com/trrep/wrapper
* OpenTravelData (OPTD) project: https://github.com/opentraveldata/opentraveldata

# Configuration

## Installation of OpenTREP
This module does not install OpenTREP, you have to do that.
On RedHat/CentOS/Fedora, OpenTREP is packaged and can therefore easily
be installed with the native packager manager (`dnf` or `yum`).

On the platforms, it can be installed by following the instructions
in the [`README.md` file](https://github.cm/trep/opeentrep/tree/master/README.md).

## Test the wrapper application

* Import the module:
```python

 >>> from OpenTrepWrapper import main_trep, index_trep
 >>> from OpenTrepWrapper import DEFAULT_LOG, DEFAULT_FMT, DEFAULT_DB

```

* Index the OPTD data file:
```python

 >>> index_trep (xapianDBPath = '/tmp/opentrep/xapian_traveldb', logFilePath = '/tmp/opentrep/opeentrep-indexer.log', verbose = False)

```

* Search:
```python

 >>> main_trep (searchString = 'nce sfo', outputFormat = 'S',  xapianDBPath = '/tmp/opentrep/xapian_traveldb',  logFilePath = '/tmp/opentrep/opeentrep-searcher.log',  verbose = False)
 ([(89.8466, 'NCE'), (357.45599999999996, 'SFO')], '')

```

* You may put the package created by `setuptools` in the repository with:
```bash
$ export TREP_VER="0.07.4"
$ export TREP_DIR="${HOME}/dev/deliveries/opentrep-latest"
$ export PYTHONPATH=${TREP_DIR}/lib/python3.7/site-packages/pyopentrep:${TREP_DIR}/lib
$ rake
```

* On MacOS, if there is an issue with the interceptors:
```bash
$ ASAN_OPTIONS=detect_container_overflow=0 \
 DYLD_INSERT_LIBRARIES=/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib \
 /usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Contents/MacOS/Python  test.py 
......
----------------------------------------------------------------------
Ran 6 tests in 2.832s

OK
```


