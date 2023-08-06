======
Verdoc
======

Deploy references from source control.

* ``verdoc`` checks out Git tags/branches/commits/etc. in temporary clones and runs::

   tox -e verdoc -- "$outdir"

* ``verdoc-index`` creates an ``index.html`` file that redirects to any URL you give it.

Only Git and tox are supported out of the box, but ``verdoc`` aims to be modular and easy to extend.

Installation
============

Use `pipx <https://pipxproject.github.io/pipx/>`__ to install ``verdoc``.

.. code:: sh

    pipx install verdoc

Usage
=====

See `the documentation <https://dmtucker.github.io/verdoc/>`__ for detailed usage instructions.

.. code:: sh

  $ git checkout --orphan gh-pages
  $ git rm -rf .
  $ git tag -l
  v1.0.0
  v2.0.0
  $ # Run `tox -e docs` instead of `tox -e verdoc`:
  $ verdoc --build-opt env=docs v1.0.0 v2.0.0
  INFO:verdoc:[v1.0.0] started
  INFO:verdoc:[v2.0.0] started
  INFO:verdoc:[v1.0.0] succeeded
  INFO:verdoc:[v2.0.0] succeeded
  $ git add v1.0.0/ v2.0.0/
  $ git commit -m "Add built docs for v1.0.0 and v2.0.0"
  $ verdoc-index v2.0.0
  $ git add index.html
  $ git commit -m "Create an index.html that redirects to v2.0.0"
  $ git push
