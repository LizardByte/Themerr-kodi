Additional Information
======================

References
----------

Kodi Built-in modules
^^^^^^^^^^^^^^^^^^^^^

- `Kodistubs <https://romanvm.github.io/Kodistubs/index.html>`__
- `Built in modules <https://kodi.wiki/view/Python_libraries#Built-in_modules>`__


Kodi References
^^^^^^^^^^^^^^^

- `Add-on development <https://kodi.wiki/view/Add-on_development>`__
- `Add-on rules <https://kodi.wiki/view/Add-on_rules>`__
- `JSON-RPC API <https://kodi.wiki/view/JSON-RPC_API>`__
- `Third party python modules <https://kodi.wiki/view/Category:Add-on_libraries/modules>`__

Similar Add-ons
^^^^^^^^^^^^^^^

- `service.tvtunes <https://github.com/latts9923/service.tvtunes>`__

Notes
-----

Kodistubs
^^^^^^^^^

`Kodistubs` is a project that provides stubs for the Kodi built-in modules. It makes it very easy to develop Kodi add-ons
in an IDE like PyCharm. This is included in the ``requirements-dev.txt``.

Python Dependencies
^^^^^^^^^^^^^^^^^^^
Python dependencies can be added in three different ways.

1. Kodi add-on modules
2. PyPI modules
3. Submodules

.. tab:: Kodi add-on modules

   The preferred method is to use Kodi add-on modules. Using this method allows the dependency to be included without
   including extra bloat.

   1. Add the dependency to the ``addon.yaml`` file in the ``addon['requires']['import']`` section.

.. tab:: PyPI modules

   If the dependency is not available as a Kodi add-on module, the next preferred method is to use PyPI modules.
   Using this method allows the dependency to be installed from PyPI when the add-on is built.

   1. Add the dependency to the ``requirements.txt`` file, and hard pin the version. e.g. ``my_requirement==1.2.3``

.. tab:: Submodules

   If the dependency is not available as a Kodi add-on module or a PyPI module, the last resort is to use submodules.

   1. Add the dependency as a submodule in the ``third-party`` directory.

      .. code-block:: bash

         git submodule add <git_url>

   2. Checkout a stable version of the dependency.

      .. code-block:: bash

         git checkout <branch, commit, or tag>

   3. Add the branch, that dependabot should track, to the ``.gitmodules`` file.

      .. code-block:: ini

         [submodule "third-party/<submodule_name>"]
             path = third-party/<submodule_name>
             url = <git_url>
             branch = <branch>

IDE Configuration
^^^^^^^^^^^^^^^^^

To allow your IDE to find dependencies which are provided by Kodi, you may be able to add the
``third-party/repo-scripts/script.module.<module_name>/lib`` directory to your IDE's sources list. In PyCharm, you can
right click the ``lib`` directory and select ``Mark Directory as`` -> ``Sources Root``. In VSCode, you can add the
following to your ``.vscode/settings.json`` file:

.. code-block:: json

   {
       "python.analysis.extraPaths": [
           "./third-party/repo-scripts/script.module.<module_name>/lib"
       ]
   }
