.. This file is auto-converted from CHANGELOG.md (make update-changelog) -- do not edit

Change log
**********
::

    ____          _           _                 _ 
   |  _ \   __ _ | |_   __ _ | |      __ _   __| |
   | | | | / _` || __| / _` || |     / _` | / _` |
   | |_| || (_| || |_ | (_| || |___ | (_| || (_| |
   |____/  \__,_| \__| \__,_||_____| \__,_| \__,_|
                                         Container

This is a high level and scarce summary of the changes between releases.
We would recommend to consult log of the `DataLad git
repository <http://github.com/datalad/datalad-container>`__ for more
details.

0.3.1 (Mar 05, 2019) – Upgrayeddd
---------------------------------

Fixes
~~~~~

-  ``containers-list`` recursion actually does recursion.

0.3.0 (Mar 05, 2019) – Upgrayedd
--------------------------------

API changes
~~~~~~~~~~~

-  ``containers-list`` no longer lists containers from subdatasets by
   default. Specify ``--recursive`` to do so.

-  ``containers-run`` no longer considers subdataset containers in its
   automatic selection of a container name when no name is specified. If
   the current dataset has one container, that container is selected.
   Subdataset containers must always be explicitly specified.

New features
~~~~~~~~~~~~

-  ``containers-add`` learned to update a previous container when passed
   ``--update``.

-  ``containers-add`` now supports Singularity’s “docker://” scheme in
   the URL.

-  To avoid unnecessary recursion into subdatasets, ``containers-run``
   now decides to look for containers in subdatasets based on whether
   the name has a slash (which is true of all subdataset containers).

0.2.2 (Dec 19, 2018) – The more the merrier
-------------------------------------------

-  list/use containers recursively from installed subdatasets
-  Allow to specify container by path rather than just by name
-  Adding a container from local filesystem will copy it now

0.2.1 (Jul 14, 2018) – Explicit lyrics
--------------------------------------

-  Add support ``datalad run --explicit``.

0.2 (Jun 08, 2018) – Docker
---------------------------

-  Initial support for adding and running Docker containers.
-  Add support ``datalad run --sidecar``.
-  Simplify storage of ``call_fmt`` arguments in the Git config, by
   benefiting from ``datalad run`` being able to work with single-string
   compound commands.

0.1.2 (May 28, 2018) – The docs
-------------------------------

-  Basic beginner documentation

0.1.1 (May 22, 2018) – The fixes
--------------------------------

.. _new-features-1:

New features
~~~~~~~~~~~~

-  Add container images straight from singularity-hub, no need to
   manually specify ``--call-fmt`` arguments.

.. _api-changes-1:

API changes
~~~~~~~~~~~

-  Use “name” instead of “label” for referring to a container (e.g.
   ``containers-run -n ...`` instead of ``containers-run -l``.

.. _fixes-1:

Fixes
~~~~~

-  Pass relative container path to ``datalad run``.
-  ``containers-run`` no longer hides ``datalad run`` failures.

0.1 (May 19, 2018) – The Release
--------------------------------

-  Initial release with basic functionality to add, remove, and list
   containers in a dataset, plus a ``run`` command wrapper that injects
   the container image as an input dependency of a command call.
