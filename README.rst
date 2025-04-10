.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/OpenStudioLandscapes-<Your-New-Feature>.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/OpenStudioLandscapes-<Your-New-Feature>
    .. image:: https://readthedocs.org/projects/OpenStudioLandscapes-<Your-New-Feature>/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://OpenStudioLandscapes-<Your-New-Feature>.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/OpenStudioLandscapes-<Your-New-Feature>/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/OpenStudioLandscapes-<Your-New-Feature>
    .. image:: https://img.shields.io/pypi/v/OpenStudioLandscapes-<Your-New-Feature>.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/OpenStudioLandscapes-<Your-New-Feature>/
    .. image:: https://img.shields.io/conda/vn/conda-forge/OpenStudioLandscapes-<Your-New-Feature>.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/OpenStudioLandscapes-<Your-New-Feature>
    .. image:: https://pepy.tech/badge/OpenStudioLandscapes-<Your-New-Feature>/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/OpenStudioLandscapes-<Your-New-Feature>
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/OpenStudioLandscapes-<Your-New-Feature>

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

======================================
OpenStudioLandscapes-<Your-New-Feature>
======================================


    OpenStudioLandscapes module template


A longer description of your project goes here...
This is a template module that can serve as a starting
point to implement new functionality in `OpenStudioLandscapes`_.

.. _OpenStudioLandscapes: https://github.com/michimussato/OpenStudioLandscapes


Installation
============


Add `OpenStudioLandscapes.<Your_New_Feature>.definitions` to
`OpenStudioLandscapes.engine.constants.THIRD_PARTY`:

.. code-block:: python

   THIRD_PARTY = [
       {
           "enabled": True,
           "module": "OpenStudioLandscapes.<Your_New_Feature>.definitions",,
           "compose_scope": ComposeScope.DEFAULT,
       },
   ]


Install module into `venv`

.. code-block:: bash

   cd OpenStudioLandscapes-<Your-New-Feature>
   pip install -e .[dev]


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
