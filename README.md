OpenTrepWrapper
===============

# Table of Content (ToC)
<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Overview
[OpenTREP](https://github.com/trep/opentrep) aims at providing a clean API,
and the corresponding C++ implementation, for parsing travel-/transport-focused
requests. It powers the https://transport-search.org Web site (as well
as its newer version, https://www2.transport-search.org).

As part of the [OpenTREP releases](https://github.com/trep/opentrep/releases),
there is a Python extension, named
[`opentrep` and published on PyPi](https://pypi.org/project/opentrep/).
That Python extension comes as a so-called binary wheel only for MacOS
(which makes it very easy to install on that platform, then).
[Contributions](https://github.com/trep/opentrep/pulls) are welcome
to also build wheels for other platforms (_e.g._, Linux, including WSL
on MS Windows). So far, for those other platforms, the Python extension
has to be built from the source distribution, also
[available on PyPi in the same place](https://pypi.org/project/opentrep/).

[OpenTrepWrapper (this project)](https://github.com/trep/wrapper) provides
a simple Python wrapper around the OpenTREP Python extension, and is also
[released on PyPi](https://pypi.org/project/OpenTrepWrapper/).

# Refefences
* OpenTREP project: https://github.com/trep/opentrep
* This GitHub project: https://github.com/trep/wrapper
* PyPi artifacts:
  + OpenTREP Python extension: https://github.com/trep/opentrep/pulls
  + OpenTREP simple Python wrapper: https://pypi.org/project/OpenTrepWrapper/
* OpenTravelData (OPTD) project: https://github.com/opentraveldata/opentraveldata
* [How to install `pyenv` and `pipenv`](https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env)
* How to setup, on your favorite Linux distribution (_e.g._, Ubuntu LTS,
  Debian or CentOS), C++-, Python- and database-related development tools:
  https://github.com/cpp-projects-showcase/docker-images
* [Twine utility](https://github.com/pypa/twine)

# Configuration

## Installation of `pyenv` and `pipenv`
* See https://github.com/machine-learning-helpers/induction-python/tree/master/installation/virtual-env
  for the details.

* Install Python:
```bash
$ pushd ~/.pyenv && git pull && popd # if pyenv is in ~/.pyenv
$ pyenv install 3.8.5 && pyenv global 3.8.5 && \
  pip install -U pip pipenv && pyenv global system
```

* Clone this Git repository:
```bash
$ mkdir -p ~/dev/geo/trep && git clone https://github.com/trep/wrapper.git ~/dev/geo/trep-wrapper
```

* Install the Python virtual environment:
```bash
$ cd ~/dev/geo/trep-wrapper
$ pipenv --rm && rm -f Pipfile.lock && \
  pipenv install && pipenv install --dev
```

## Installation of OpenTREP
This module does not install OpenTREP itself; the overview gives the general
procedure on how to do it.

Also, on RedHat/CentOS/Fedora, OpenTREP is packaged and can therefore easily
be installed with the native packager manager (`dnf` or `yum`).

Alternatively, on most of the platforms, it can be installed by following
the instructions in the
[OpenTREP `README.md` file](https://github.com/trep/opentrep/tree/master/README.md).
* Basically, a few C++-, Python- and database-related development tools
  have to be installed. The
  [Docker images for C++ projects GitHub repository](https://github.com/cpp-projects-showcase/docker-images)
  gives all the details in the `Dockerfile` of the corresponding Linux
  distribution folders, _e.g._,
  [`ubuntu2004/Dockerfile`](https://github.com/cpp-projects-showcase/docker-images/blob/master/ubuntu2004/Dockerfile)
  for Ubuntu 20.04 LTS (Focal Fossa).

* And then the OpenTREP Python extension may simply be installed with `pip`
  (either invoked through the native Python interpreter or through `pipenv`
  with a Python interpreter installed by `pyenv`).

* Note that the OpenTREP Python extension is not referred to in the
  [`Pipfile` file](https://github.com/trep/wrapper/blob/master/Pipfile),
  in order to have a minimum viable Python virtual environment installed
  by `pipenv`. If `opentrep` were referred to in the `Pipfile` file,
  the installation of the Python virtual environment may just stop in
  error after an attempt to compile the OpenTREP Python extension,
  and it would be hard to debug, without evenhaving a minimal viable
  Python virtual environment.

* Once the Python virtual environment has been installed with `pipenv`,
  The installation of the OpenTREP Python extension should go something like:
```bash
user@laptop$ pipenv shell
Launching subshell in virtual environment…
(trep-wrapper-FkiBIXof) ✔ python -V
Python 3.8.5
(trep-wrapper-FkiBIXof) ✔ pip install -U opentrep
Collecting opentrep
  Using cached opentrep-0.7.7.post6-cp38-cp38-macosx_10_15_x86_64.whl (10.3 MB)
Installing collected packages: opentrep
Successfully installed opentrep-0.7.7.post6
(trep-wrapper-FkiBIXof) ✔ exit
```

* Check that the OpenTREP Python extension (`opentrep`) has been installed
  properly: 
```bash
user@laptop$ pipenv run python -mpip freeze|grep opentrep
opentrep==0.7.7.post6
$ pipenv run python -mpip show opentrep
Name: opentrep
Version: 0.7.7.post6
Summary: Simple Python wrapper for OpenTREP
Home-page: https://github.com/trep/opentrep
Location: ~/.local/share/virtualenvs/trep-wrapper-FkiBIXof/lib/python3.8/site-packages
```

* Set a few environment variables accordingly:
```bash
$ export TREP_VENV="${HOME}/.local/share/virtualenvs/trep-wrapper-FkiBIXof"
$ export PYTHONPATH="${TREP_VENV}/lib:${TREP_VENV}/lib/python3.8/site-packages/pyopentrep"
$ export LD_LIBRARY_PATH="${TREP_VENV}/lib"
$ export PATH="${TREP_VENV}/bin:${PATH}"
```

* Alternatively, if OpenTREP, including its Python extension, has been
  installed from the sources, the environment variables would rather be:
```bash
$ export TREP_DIR="${HOME}/dev/deliveries/opentrep-latest"
$ export PYTHONPATH="${TREP_DIR}/lib/python3.8/site-packages/pyopentrep:${TREP_DIR}/lib"
$ export LD_LIBRARY_PATH="${TREP_DIR}/lib"
$ export PATH="${TREP_DIR}/bin:${PATH}"
```

* As a reminder, on MacOS,
  + OpenTREP may be installed with `pip`, without any virtual environment
   (as it does not play well with the MacOS Python so-called framework):
```bash
$ python3 -mpip uninstall -y opentrep
$ python3 -mpip install -U opentrep
```
  + The envrionment variables become:
```bash
$ export PYTHONPATH=/usr/local/lib/python3.8/site-packages/pyopentrep:/usr/local/lib
$ export DYLD_LIBRARY_PATH=/usr/local/lib
```

* For the remaining of this document, it is assumed that OpenTREP has been
  installed by `pip`, either with the native Python framework (MacOS)
  or with `pipenv` (Linux, including WSL on MS Windows)

### Download the OpenTravelData (OPTD) data and index them
* Download the OpenTravelData:
```python
>>> import opentraveldata
>>> myOPTD = opentraveldata.OpenTravelData()
>>> myOPTD.downloadFilesIfNeeded()
>>> myOPTD
OpenTravelData:
        Local IATA/ICAO POR file: /tmp/opentraveldata/optd_por_public_all.csv
        Local UN/LOCODE POR file: /tmp/opentraveldata/optd_por_unlc.csv
>>> myOPTD.fileSizes()
(44044195, 4888086)
```

* Initialize the Xapian index with the `-i` option of `pyopentrep.py`,
  so as to index the full OpenTravelData (OPTD) POR (points of reference)
  data file
  + On Linux:
```bash
$ pipenv run python ${TREP_VENV}/lib/python3.8/site-packages/pyopentrep/pyopentrep.py -p /tmp/opentraveldata/optd_por_public_all.csv -i
```
  + On MacOS:
```bash
$ DYLD_INSERT_LIBRARIES=/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib ASAN_OPTIONS=detect_container_overflow=0 /usr/local/Cellar/python\@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python /usr/local/lib/python3.8/site-packages/pyopentrep/pyopentrep.py -p /tmp/opentraveldata/optd_por_public_all.csv -i
```
```bash
OPTD-maintained list of POR (points of reference): '/tmp/opentraveldata/optd_por_public_all.csv'
Xapian-based travel database/index: '/tmp/opentrep/xapian_traveldb0'
SQLite database: '/tmp/opentrep/sqlite_travel.db'
Perform the indexation of the (Xapian-based) travel database.
That operation may take several minutes on some slow machines.
It takes less than 20 seconds on fast ones...
Number of actually parsed records: 1,000, out of 103,394 records in the POR data file so far
...
Number of actually parsed records: 20,000, out of 122,394 records in the POR data file so far
Done. Indexed 20335 POR (points of reference)
```

### Test of the OpenTREP Python extension
* Start the Python interpreter on Linux:
```bash
$ pipenv run python
```

* Start the Python interpreter on MacOS:
```bash
$ DYLD_INSERT_LIBRARIES=/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib ASAN_OPTIONS=detect_container_overflow=0 /usr/local/Cellar/python\@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python
```

* Test the OpenTREP Python extension:
```python
>>> import pyopentrep
>>> openTrepLibrary = pyopentrep.OpenTrepSearcher()
>>> initOK = openTrepLibrary.init ('/tmp/opentraveldata/optd_por_public.csv', '/tmp/opentrep/xapian_traveldb', 'sqlite', '/tmp/opentrep/sqlite_travel.db', 0, False, True, True, 'pyopentrep.log')
>>> initOK
True
>>> openTrepLibrary.search('S', 'nce sfo')
'NCE/0,SFO/0'
```

## Test the wrapper application
* In the following Python examples, it is assumed that an interactive
  Python Shell has been launched:
```bash
$ pipenv run python
Python 3.8.5 (default, Jul 24 2020, 13:35:18) 
>>> 
```

* Or, on MacOS:
```bash
$ ASAN_OPTIONS=detect_container_overflow=0 \
 DYLD_INSERT_LIBRARIES=/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/lib/darwin/libclang_rt.asan_osx_dynamic.dylib \
 /usr/local/Cellar/python\@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python
Python 3.8.5 (default, Jul 24 2020, 13:35:18) 
>>> 
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
 /usr/local/Cellar/python\@3.8/3.8.5/Frameworks/Python.framework/Versions/3.8/Resources/Python.app/Contents/MacOS/Python test.py
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
total 56
-rw-r--r--  1 user  staff   7.7K Mar  2 11:14 OpenTrepWrapper-0.7.7.post1-py3-none-any.whl
-rw-r--r--  1 user  staff   7.3K Mar  2 11:14 OpenTrepWrapper-0.7.7.post1-py3.8.egg
-rw-r--r--  1 user  staff   8.4K Mar  2 11:14 OpenTrepWrapper-0.7.7.post1.tar.gz
```

* Publish to PyPi:
```bash
$ pipenv run twine upload -u __token__ dist/*
```


