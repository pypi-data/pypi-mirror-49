""" Syncurity Utils package

This package provides a common library of utilities and models that are useful across Syncurity's library of Stackstorm
packs.

:copyright: (c) 2019 Syncurity
:license: Apache 2.0, see LICENSE.txt for more details
"""

# Default logger configuration
import logging
from logging import NullHandler

from .__version__ import __author__, __author_email__, __license__
from .__version__ import __copyright__
from .__version__ import __description__, __title__, __version__

# Classes
from .models import Alert, FactGroup, Incident, Step, Task
from .utils import DecodeProofpointURL

# Functions
from .api import send_facts
from .typecheck import typecheck
from .utils import find_domain, get_fact_group_id, setup_logging

logging.getLogger(__name__).addHandler(NullHandler())

__all__ = ['Alert', 'DecodeProofpointURL', 'FactGroup', 'Incident', 'Step', 'Task', 'find_domain', 'get_fact_group_id',
           'send_facts', 'setup_logging', 'typecheck']
