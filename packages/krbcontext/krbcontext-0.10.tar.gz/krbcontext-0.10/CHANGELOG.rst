ChangeLog
=========

0.10 (2019-07-15)
-----------------

- Use set_default when storing credentials (Michael Simacek)

0.9 (2019-06-20)
----------------

- Fix .travis.yml to use Python 3.7 (Chenxiong Qi)
- Update docs/source/conf.py to read package info properly (Chenxiong Qi)
- Add Python 3.7 to and remove Python 3.5 from TravisCI (Chenxiong Qi)
- Update scripts (Chenxiong Qi)
- Ignore more directories from git (Chenxiong Qi)
- Remove testenv py34 and py35 (Chenxiong Qi)
- Add testenv py37 (Chenxiong Qi)
- Fix typo in comment (Chenxiong Qi)
- Fix renewing expired FILE ccache (Michael Simacek)
- Remove flake8 from BuildRequires from SPEC (Chenxiong Qi)

0.8 (2017-09-05)
----------------

- Fix SPEC (Chenxiong Qi)
- Use __future__.absolute_import (Chenxiong Qi)
- Fix and enhance maintanence scripts (Chenxiong Qi)

0.7 (2017-08-30)
----------------

- Remove unused meta info (Chenxiong Qi)
- Fix init_with_keytab and tests (Chenxiong Qi)
- Add script for publishing packages (Chenxiong Qi)
- Refine make release script (Chenxiong Qi)

0.6 (2017-08-27)
----------------

- Fix reading package info (Chenxiong Qi)

0.5 (2017-08-27)
----------------

- Add script for making release (Chenxiong Qi)
- Add distcheck to Makefile (Chenxiong Qi)
- Refine doc settings (Chenxiong Qi)
- Easy to set project info (Chenxiong Qi)
- Bump version to 4.0 in doc (Chenxiong Qi)

0.4 (2017-08-26)
================

- Migrate to python-gssapi
- Compatible with Python 3

0.3.3 (2014-03-12)
------------------

- Change README.txt to README.rst
- Fix: logic error of KRB5CCNAME maintenance during initialization
- Fix testcase of getting default credential cache

0.3.2 (2013-06-15)
------------------

- Add LICENSE

0.3.1 (2013-01-18)
------------------

- Thread-safe credentials cache initialization

0.3.0 (2013-01-10)
------------------

- Lazy initialization of credential cache.
- Refactor all code
- Rewrite all unittest
- Improve SPEC
- Improve configuration of Python package distribution
- Update documentation

0.2.1 (2012-08-02)
------------------

- Remove dependency to setuptools
- Rewrite SPEC file for packaging RPM in Fedora and RHEL
- Using VERSION.txt to share the version between setup.py and SPEC file

0.2 (2012-03-19)
----------------

- Add change log to project

- Providing RPM distribution package

0.1 (2012-03-19)
----------------

- Upload to PyPI

- Add more information to setup.py after initialized import to github
