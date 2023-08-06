#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Testskript.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>

"""

# -----------------------------------------------------------------------------
# -- Modul importe
# - standart Module
import logging

# - zusätzliche Module

# - eigene Module
from mrdevtools import timeit_long, timeit_short

# -----------------------------------------------------------------------------
# -- Modul Definitionen
# -- Konstanten
# -- Klassen
# - Fehlerklassen
# - "Arbeitsklassen"


# -- Funktionen
@timeit_short
@timeit_long
def tests(n: int = 1) -> None:
    """Testskript."""
    for x in range(n):
        print(x)


# -----------------------------------------------------------------------------
# -- modul test
if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    logging.basicConfig(filename='basictests.log', level=logging.DEBUG)
    logging.info("start tests")
    tests(1)
    tests(10)
    tests(100)
    tests(1000)
    tests(10000)
    logging.info("ende tests")
