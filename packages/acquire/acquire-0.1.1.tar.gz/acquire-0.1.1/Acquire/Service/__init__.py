"""
Acquire : (C) Christopher Woods 2018

This module provides the base classes and functions used to define
the services used in the system. It is not likely to be user-facing
"""

from ._function import *
from ._get_session_info import *
from ._get_services import *
from ._get_service_account_bucket import *
from ._service_account import *
from ._service import *
from ._profile import *
from ._errors import *
from ._cache_management import *
from ._trust_service import *

try:
    if __IPYTHON__:
        def _set_printer(C):
            """Function to tell ipython to use __str__ if available"""
            get_ipython().display_formatter.formatters['text/plain'].for_type(
                C,
                lambda obj, p, cycle: p.text(str(obj) if not cycle else '...')
                )

        import sys as _sys
        import inspect as _inspect

        _clsmembers = _inspect.getmembers(_sys.modules[__name__],
                                          _inspect.isclass)

        for _clsmember in _clsmembers:
            _set_printer(_clsmember[1])
except:
    pass
