mrdevtools - helper tools
=========================

Hilfsmittel beim Entwickeln von Python Programmen.

Usage
-----



License
-------

GNU AFFERO GENERAL PUBLIC LICENSE Version 3

Developer guide
---------------

Upgrade your setup tools and pip.
They are needed for development and testing only:

.. code:: bash

   pip install --upgrade setuptools pip wheel

Development steps for code changes

.. code:: bash

   git clone https://gitlab.com/anatas_ch/pyl_mrdevtools.git
   cd pyl_mrdevtools
   pip install -e .

Then install relevant development requirements:

.. code:: bash

   pip install -r requirements_rnd.txt

`docs` folder contains theme's own documentantion.

.. code:: bash

   cd docs
   make clean; make html

Once you have finished your changes, please provide test case(s) and relevant documentation.
