========================
sphinxcontrib-odfbuilder
========================

Open Document Format builder

Overview
--------

A Sphinx builder for OpenDocument Text (.odt).

At this stage the builder just utilises docutils reStructuredText to ODT capabilities, and doesn't support any Sphinx specific markup constructs.

Once installed, the builder can be invoked by running
```
make odt
```
in the top level folder of a Sphinx project.

This extension was generated using the sphinx-contrib cookiecutter, but is not currently part of the sphinx-contrib project.

Build
-----

```
python setup.py build
```

Distribute
----------

```
python setup.py sdist
```

Install
-------

```
pip install --upgrade sphinx
wget https://github.com/mans0954/odfbuilder/releases/download/0.0.1/sphinxcontrib-odfbuilder-0.0.1.tar.gz
pip install sphinxcontrib-odfbuilder-0.0.1.tar.gz
```

Links
-----

- Source: https://github.com/sphinx-contrib/sphinxcontrib-odfbuilder
- Bugs: https://github.com/sphinx-contrib/sphinxcontrib-odfbuilder/issues
