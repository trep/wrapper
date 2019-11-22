OpenTrepWrapper
===============

# Refefences
* OpenTREP project: https://github.com/trep/opentrep
* This GitHub project: https://github.com/trep/wrapper
* OpenTravelData (OPTD) project: https://github.com/opentraveldata/opentraveldata
* [How to install `pyenv` and `pipenv`](https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env)

# Configuration

## Installation of OpenTREP
This module does not install OpenTREP, you have to do that.
On RedHat/CentOS/Fedora, OpenTREP is packaged and can therefore easily
be installed with the native packager manager (`dnf` or `yum`).

On the platforms, it can be installed by following the instructions
in the [`README.md` file](https://github.com/trep/opentrep/tree/master/README.md).

For the remaining of this document, it assumed that OpenTREP has been
installed from the sources in `${HOME}/dev/deliveries/opentrep-latest`.
You can easily customize the `PYTHONPATH` and `LD_LIBRARY_PATH`
environment variables to suit your own settings.

* You may put the package created by `setuptools` in the repository with:
```bash
$ export TREP_DIR="${HOME}/dev/deliveries/opentrep-latest"
$ export PYTHONPATH="${TREP_DIR}/lib/python3.7/site-packages/pyopentrep:${TREP_DIR}/lib"
$ export LD_LIBRARY_PATH="${TREP_DIR}/lib"
$ export PATH="${TREP_DIR}/bin:${PATH}"
```

## Installation of `pyenv` and `pipenv`
* Install Python:
```bash
$ pyenv install 3.7.4
$ pyenv global 3.7.4 && pip install -U pip pipenv && pyenv global system
```

* Clone this Git repository:
```bash
$ mkdir -p ~/dev/geo/trep && git clone https://github.com/trep/wrapper.git ~/dev/geo/trep/wrapper
```

* Install the Python virtual environment:
```bash
$ cd ~/dev/geo/trep/wrapper
$ pipenv install && pipenv install --dev
```

## Test the wrapper application
* In the following Python examples, it is assumed that an interactive
  Python Shell has been launched:
```bash
$ pipenv run python
```

* Or, on MacOS:
```bash
$ ASAN_OPTIONS=detect_container_overflow=0 \
 DYLD_INSERT_LIBRARIES=/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib \
 /usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Contents/MacOS/Python
```

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

* End the Python session:
```python

 >>> quit()

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

# Release OpenTrepWrapper to PyPi
* Build the Python artifacts for OpenTrepWrapper:
```bash
$ rm -rf dist && mkdir dist
$ pipenv run python setup.py sdist bdist_wheel bdist_egg
$ ls -lFh dist
total 48
-rw-r--r--  1 user  staff   7.1K Nov 22 01:03 OpenTrepWrapper-0.7.4.post3-py3-none-any.whl
-rw-r--r--  1 user  staff   6.7K Nov 22 01:03 OpenTrepWrapper-0.7.4.post3-py3.7.egg
-rw-r--r--  1 user  staff   6.2K Nov 22 01:03 OpenTrepWrapper-0.7.4.post3.tar.gz
```

* Publish to PyPi:
```bash
$ pipenv run twine upload dist/*
```


