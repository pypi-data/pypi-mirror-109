# -*- coding: utf-8 -*-

"""
Hilfmittel zum entwickeln.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>

"""

# -----------------------------------------------------------------------------
# -- Modul importe
# - standart Module
from typing import Optional
import logging

# - zusätzliche Module

# - eigene Module

# -----------------------------------------------------------------------------
# -- Modul Definitionen

# -- Konstanten
LOG_COLOR_CODES = {
    logging.CRITICAL: "\033[1;35m",  # bright/bold magenta
    logging.ERROR: "\033[1;31m",  # bright/bold red
    logging.WARNING: "\033[1;33m",  # bright/bold yellow
    logging.INFO: "\033[0;37m",  # white /light gray
    logging.DEBUG: "\033[1;30m"   # bright/bold black / dark gray
}

LOG_RESET_CODE = "\033[0m"

# -- Klassen
# - Fehlerklassen


# - "Arbeitsklassen"
class LogColorFormatter(logging.Formatter):
    """Formatter Class for colored logging output.

    Parameters
    ----------
    fmt
        see: :class:`logging.Formatter`
    datefmt
        see: :class:`logging.Formatter`
    style
        see: :class:`logging.Formatter`
    color
        `True` colored output

    Examples
    --------
    .. code-block:: python

       colorama.init()

       console_handler = logging.StreamHandler(sys.stdout)
       console_handler.setLevel(logging.INFO)
       console_formatter = LogColorFormatter(
         fmt="%(color_on)s[%(levelname)-8s]%(color_off)s %(message)s",
         color=True
       )
       console_handler.setFormatter(console_formatter)

       logging.basicConfig(format="%(asctime)s [%(levelname)-8s] %(message)s",
                           level=logging.INFO,
                           handlers=[
                               logging.FileHandler("cpds.log"),
                               console_handler
                           ],
                           )

    See Also
    --------
    :mod:`logging`

    References
    ----------
    * https://gist.github.com/fonic/7e5ab76d951a2ab2d5f526a7db3e2004
    * https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout

    """

    def __init__(self,
                 *,
                 fmt: Optional[str] = None,
                 datefmt: Optional[str] = None,
                 style: str = '%',
                 color: bool = False) -> None:
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.color = color

    def format(self, record: logging.LogRecord) -> str:
        """Format the specified record as text."""
        if (self.color and record.levelno in LOG_COLOR_CODES):
            record.color_on = LOG_COLOR_CODES[record.levelno]       # type: ignore[attr-defined]
            record.color_off = LOG_RESET_CODE       # type: ignore[attr-defined]
        else:
            record.color_on = ""       # type: ignore[attr-defined]
            record.color_off = ""       # type: ignore[attr-defined]
        return super().format(record)


# -- Funktionen

# -----------------------------------------------------------------------------
# -- modul test
if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    pass
