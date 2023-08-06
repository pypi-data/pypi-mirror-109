.. _stginga-install:

Installation
============

``stginga`` requires:

* Python 3.7 or later
* Astropy 3.0 or later
* SciPy 0.18 or later
* Ginga 2.7 or later, see
  `Ginga's documentation <https://ginga.readthedocs.io/>`_

We suggest using `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ as a
Python distribution that is known to work with ``stginga``::

    conda install stginga -c conda-forge

or::

    conda install stginga -c http://ssb.stsci.edu/astroconda

Alternately, ``stginga`` 0.3 and beyond is also available on PyPI::

    pip install stginga

If you wish to install the development version instead::

    pip install git+https://github.com/spacetelescope/stginga.git@master
