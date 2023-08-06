==========
🐵  bonobo
==========

Data-processing for humans.

.. image:: https://img.shields.io/pypi/v/bonobo.svg
    :target: https://pypi.python.org/pypi/bonobo
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/bonobo.svg
    :target: https://pypi.python.org/pypi/bonobo
    :alt: Versions

.. image:: https://readthedocs.org/projects/bonobo/badge/?version=master
    :target: http://docs.bonobo-project.org/
    :alt: Documentation

.. image:: https://travis-ci.org/python-bonobo/bonobo.svg?branch=master
    :target: https://travis-ci.org/python-bonobo/bonobo
    :alt: Continuous Integration (Linux)

.. image:: https://ci.appveyor.com/api/projects/status/github/python-bonobo/bonobo?retina=true&branch=master&svg=true
    :target: https://ci.appveyor.com/project/hartym/bonobo?branch=master
    :alt: Continuous Integration (Windows)

.. image:: https://codeclimate.com/github/python-bonobo/bonobo/badges/gpa.svg
   :target: https://codeclimate.com/github/python-bonobo/bonobo
   :alt: Code Climate

.. image:: https://img.shields.io/coveralls/python-bonobo/bonobo/master.svg
    :target: https://coveralls.io/github/python-bonobo/bonobo?branch=master
    :alt: Coverage

Bonobo is an extract-transform-load framework for python 3.5+ (see comparisons with other data tools).

Bonobo uses plain old python objects (functions, generators and iterators), allows them to be linked together in a directed graph, and then executed using a parallelized strategy, without having to worry about the underlying complexity.

Developers can focus on writing simple and atomic operations, that are easy to unit-test by-design, while the focus of the
framework is to apply them concurrently to rows of data.

One thing to note: write pure transformations and you'll be safe.

Bonobo is a young rewrite of an old python2.7 tool that ran millions of transformations per day for years on production.
Although it may not yet be complete or fully stable (please, allow us to reach 1.0), the basics are there.

----

*Bonobo is under heavy development, we're doing our best to keep the core as stable as possible while still moving forward. Please allow us to reach 1.0 stability and our sincere apologies for anything we break in the process (feel free to complain on issues, allowing us to correct breakages we did not expect)*

----

Homepage: https://www.bonobo-project.org/ (`Roadmap <https://www.bonobo-project.org/roadmap>`_)

Documentation: http://docs.bonobo-project.org/

Contributing guide: http://docs.bonobo-project.org/en/latest/contribute/index.html

Issues: https://github.com/python-bonobo/bonobo/issues

Slack: https://bonobo-slack.herokuapp.com/

Release announcements: http://eepurl.com/csHFKL

----

Made with ♥ by `Romain Dorgueil <https://twitter.com/rdorgueil>`_ and `contributors <https://github.com/python-bonobo/bonobo/graphs/contributors>`_.

.. image:: https://img.shields.io/pypi/l/bonobo.svg
    :target: https://pypi.python.org/pypi/bonobo
    :alt: License


