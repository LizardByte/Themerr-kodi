Testing
=======

Flake8
------
Themerr-kodi uses `Flake8 <https://pypi.org/project/flake8/>`__ for enforcing consistent code styling. Flake8 is
included in the ``requirements-dev.txt``.

The config file for flake8 is ``.flake8``. This is already included in the root of the repo and should not be modified.

Test with Flake8
   .. code-block:: bash

      python -m flake8

Sphinx
------
Themerr-kodi uses `Sphinx <https://www.sphinx-doc.org/en/master/>`__ for documentation building. Sphinx is included
in the ``requirements-dev.txt``.

Themerr-kodi follows `numpydoc <https://numpydoc.readthedocs.io/en/latest/format.html>`__ styling and formatting in
docstrings. This will be tested when building the docs. `numpydoc` is included in the ``requirements-dev.txt``.

The config file for Sphinx is ``docs/source/conf.py``. This is already included in the root of the repo and should not
be modified.

Test with Sphinx
   .. code-block:: bash

      cd docs
      make html

   Alternatively

   .. code-block:: bash

      cd docs
      sphinx-build -b html source build

Lint with rstcheck
   .. code-block:: bash

      rstcheck -r .

pytest
------
Themerr-kodi uses `pytest <https://pypi.org/project/pytest/>`__ for unit testing. pytest is included in the
``requirements-dev.txt``.

No config is required for pytest.

Test with pytest
   .. code-block:: bash

      python -m pytest -rxXs --tb=native --verbose --cov=src tests
