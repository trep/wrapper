
import io
import os
import glob
import setuptools

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

setuptools.setup(
    name = 'OpenTrepWrapper',
    version = '0.7.7.post2',
    author = 'Denis Arnaud',
    author_email = 'denis.arnaud_fedora@m4x.org',
    url = 'https://github.com/trep/wrapper',
    description = 'A Python wrapper module for OpenTrep',
    long_description = read('README.md'),
    long_description_content_type = 'text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://opentrep.readthedocs.io/en/latest/',
        'Changelog': 'https://opentrep.readthedocs.io/en/latest/opentrep.html',
        'Issue Tracker': 'https://github.com/trep/wrapper/issues',
    },
    keywords=[
        'data', 'trep', 'request', 'parser', 'travel', 'transport',
        'search', 'wrapper', 'optd', 'opentraveldata', 'opentrep'
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    install_requires=[
        # 'some--package',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points = {
        'console_scripts' : [
            'OpenTrep = OpenTrepWrapper.cli:main',
        ]
    },
)

