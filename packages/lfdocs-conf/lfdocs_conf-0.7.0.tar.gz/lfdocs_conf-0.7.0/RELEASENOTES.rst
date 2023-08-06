===========
lfdocs_conf
===========

.. _lfdocs_conf_v0.7.0:

v0.7.0
======

.. _lfdocs_conf_v0.7.0_Other Notes:

Other Notes
-----------

.. releasenotes/notes/conventional_commit-5cbbd021edc324c2.yaml @ 2b9411e8831f17cfc0ad46a91886df4dcfdf04ad

- Conventional Commit message subject lines are now enforced. This affects
  CI. Additionally, if developers want to protect themselves from CI failing
  on this please make sure of the following
  
  * you have pre-commit installed
  * that you have run
    pre-commit install --hook-type commit-msg


.. _lfdocs_conf_v0.6.0:

v0.6.0
======

.. _lfdocs_conf_v0.6.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/sphinx-3.2-8e24c17b03786cfd.yaml @ a9582a78dc4fc483205ccb1cda4a58a21f690bca

- Sphinx has been upgraded to 3.2.x.

.. releasenotes/notes/unpin-more-itertools-5dff9b6955769e99.yaml @ de2a88d3f717d49863d524a2a6be4fe189bae2fb

- If using Python 3.4 or newer, more-itertools is no longer pinned to the 5.x
  release.


.. _lfdocs_conf_v0.6.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/remove-pytest-dep-8a0d427bfcd1f5c3.yaml @ caa0ac6dd799b3f782d6958001cbf8394a29e4f8

- Pytest is no longer pulled in as a dependency of docs-conf.


.. _lfdocs_conf_v0.5.0:

v0.5.0
======

.. _lfdocs_conf_v0.5.0_New Features:

New Features
------------

.. releasenotes/notes/support-sphinx-tabs-7a9e3e9ed2a7795a.yaml @ eb1f1edbd595c8fdbe25e9b693030e95fec38816

- Add support for sphinx-tabs (https://github.com/djungelorm/sphinx-tabs).


.. _lfdocs_conf_v0.5.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/update-sphinx-3.0.4-c023706bfba48a52.yaml @ d3cc1c40f6d0827686d34387d99f0d450ff4b84d

- Updates Sphinx from ~2.3.1 to ~3.0.4 which may or may not affect
  project docs build. Refer to upstream release note as necessary.
  https://www.sphinx-doc.org/en/master/changes.html


.. _lfdocs_conf_v0.3.0:

v0.3.0
======

.. _lfdocs_conf_v0.3.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/sphinx-update-6b451b2462799591.yaml @ c86baade9f3d38e9664bb617b9ea80ca01ac895e

- Sphinx version is updated from ~1.7.9 to ~1.8.5 which may or may not affect
  project docs build. Refer to upstream release note as necessary.
  https://www.sphinx-doc.org/en/master/changes.html

