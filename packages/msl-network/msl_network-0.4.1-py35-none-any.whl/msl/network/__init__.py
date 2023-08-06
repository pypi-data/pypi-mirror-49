"""
Concurrent and asynchronous network I/O.
"""
import re
from collections import namedtuple

from .client import (
    connect,
    LinkedClient,
)
from .service import Service
from .exceptions import MSLNetworkError
from .database import (
    ConnectionsTable,
    HostnamesTable,
    UsersTable,
)

__author__ = 'Measurement Standards Laboratory of New Zealand'
__copyright__ = '\xa9 2017 - 2019, ' + __author__
__version__ = '0.4.1'

_v = re.search(r'(\d+)\.(\d+)\.(\d+)[.-]?(.*)', __version__).groups()

version_info = namedtuple('version_info', 'major minor micro releaselevel')(int(_v[0]), int(_v[1]), int(_v[2]), 'final')
""":obj:`~collections.namedtuple`: Contains the version information as a (major, minor, micro, releaselevel) tuple."""
