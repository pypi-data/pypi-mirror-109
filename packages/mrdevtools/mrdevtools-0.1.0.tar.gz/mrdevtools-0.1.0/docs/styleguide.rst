************************************
Coding and Documentation Style Guide
************************************

This document contains a style guide for Python programming.  The coding style follows the
recommendations from [pep8]_ with some differences outlined here.  The documentation style is
inspiriert by the [numpydoc]_.  This document assumes the use of Python 3.

.. admonition:: And, by the way...

   Code are written to read by humans and only incidental interpreted by a computer.

Coding Style
============

Global Variable

Naming Conventions
------------------

.. Note:: Never use ``l``, ``O``, or ``I`` single letter names as these can be mistaken for ``1`` and ``0``,
          depending on typeface:

          .. code-block:: python
              :caption: Python

              O = 2    # This may look like you're trying to reassign 2 to zero


================================== ========== ==================
Name                               Formatting Used for
================================== ========== ==================
single lowercase letter            b
single uppercase letter            B
lowercase                          twowords   package, module
lower_case_with_underscores        two_words  function, varibale
UPPERCASE                          TWOWORDS
UPPER_CASE_WITH_UNDERSCORES        TWO_WORDS  constants
CapitalizedWords                   TwoWords   classes
mixedCase                          twoWords
Capitalized_Words_With_Underscores Two_Words
================================== ========== ==================



Package and Module Names
^^^^^^^^^^^^^^^^^^^^^^^^

* start with a letter
* lower case
* starts with a underline only for «non public» moduls in a package
* a…z|0…9|_

Class Names
^^^^^^^^^^^

* CamelCase

Exception Names
^^^^^^^^^^^^^^^

Global Variable Names
^^^^^^^^^^^^^^^^^^^^^

Function and Variable Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* lower case
* start with a letter
* underline to improve the readlibity
* a…z|0…9|_
* starts with a underline only for «non public» function in a module

Function and Method Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Always use `self` for the first argument to instance methods.

Always use `cls` for the first argument to class methods.

Method Names and Instance Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Constants
^^^^^^^^^

* upper case
* underline to improve the readlibity


Code Layout
-----------

Blanke Lines
^^^^^^^^^^^^
* Surround top-level functions and classes with two blank lines.

* Surround method definitions inside classes with a single blank line.

* Use blank lines sparingly inside functions to show clear steps.



Documentation Style
===================

A documentation string (docstring) is a string that describes a module, function, class, or method
definition. The docstring is a special attribute of the object (`object.__doc__`) and, for
consistency, is surrounded by triple double quotes, i.e.:



This document describes the syntax and best practices for docstrings used with the [napoleon]_
extension for [sphinx]_.

This section is a compilation from the documentation of the [napoleon]_ and [numpydoc]_ extetions.





Examples in docstrings
----------------------

These are written in `doctest <https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html>`_
format, and should illustrate how to use the function.

If posible every example should work on it's one.  The benevit is that the examples can tested with
the command:

.. code-block:: console

   [docs]$ make doctest


References
==========

.. [pep8] PEP 8, Style Guide for Python Code; Guido van Rossum, Barry
          Warsaw, Nick Coghlan, https://www.python.org/dev/peps/pep-0008/

.. [sphinx] Sphinx, Python Documentaion Generator, https://www.sphinx-doc.org/

.. [napoleon] ``sphinx.ext.napoleon`` – Support for NumPy and Google style docstrings,
              https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html

.. [numpydoc] numpydoc docstring guide, https://numpydoc.readthedocs.io/
