Installation
============

Requirements
------------

- Python 3.x
- Python packages `numpy` and `click`
- Command-line utilities `sort` (the Unix version), `bgzip` (shipped with `tabix`) 
  and `samtools`. If available, `pairtools` can compress outputs with `pbgzip` and `lz4`.

Install using conda
-------------------

We highly recommend using the `conda` package manager to install pre-compiled
`pairtools` together with all its dependencies. To get it, you can either 
install the full `Anaconda <https://www.continuum.io/downloads>`_ Python 
distribution or just the standalone 
`conda <http://conda.pydata.org/miniconda.html>`_ package manager.

With `conda`, you can install pre-compiled `pairtools` and all of its
dependencies from the `bioconda <https://bioconda.github.io/index.html>`_ channel:

.. code-block:: bash

    $ conda install -c conda-forge -c bioconda pairtools

Install using pip
-----------------

Alternatively, compile and install `pairtools` and its Python dependencies from
PyPI using pip:

.. code-block:: bash

    $ pip install pairtools


Install the development version
-------------------------------

Finally, you can install the latest development version of `pairtools` from
github. First, make a local clone of the github repository:

.. code-block:: bash

    $ git clone https://github.com/mirnylab/pairtools 

Then, you can compile and install `pairtools` in 
`the development mode <https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode>`_, 
which installs the package without moving it to a system folder and thus allows
immediate live-testing any changes in the python code. Please, make sure that you 
have `cython` installed!

.. code-block:: bash

    $ cd pairtools 
    $ pip install -e ./


