Build
=====
Follow the steps below to build the add-on.

Clone
-----
Ensure `git <https://git-scm.com/>`__ is installed and run the following:

   .. code-block:: bash

      git clone --recurse-submodules https://github.com/lizardbyte/themerr-kodi.git
      cd ./themerr-kodi

Setup venv
----------
It is recommended to setup and activate a `venv`_.

Install Requirements
--------------------
Install Requirements (Optional)
   .. code-block:: bash

      python -m pip install -r requirements.txt

Development Requirements (Required)
   .. code-block:: bash

      python -m pip install -r requirements-dev.txt

Build Add-on
------------
.. code-block:: bash

   python -m scripts.build

Remote Build
------------
It may be beneficial to build remotely in some cases. This will enable easier building on different operating systems.

#. Fork the project
#. Activate workflows
#. Trigger the `CI` workflow manually
#. Download the artifacts from the workflow run summary

.. _venv: https://docs.python.org/3/library/venv.html
