Development and Testing
=======================

.. contents::
   :depth: 1
   :local:
   :backlinks: none


Development Setup
-----------------

Create a conda environment::

    conda create -y -n pyobistools python=3.9
    conda activate pyobistools
    conda install -y -c conda-forge --file requirements.txt --file tests/requirements.txt

Run tests::

    pytest

Run pre-commit before sending in a merge request to speed up review time::

    pre-commit run --all-files


Documentation Setup
-------------------

Build docs::

    conda create -y -n pyobistools_docs python=3.9
    conda activate pyobistools_docs
    conda install -y -c conda-forge --file docs/requirements.txt
    cd docs
    make livehtml

Then open a browser to `http://localhost:8000 <http://localhost:8000>`_. The documentation will update in the browser as you make changes and save the documentation files.
