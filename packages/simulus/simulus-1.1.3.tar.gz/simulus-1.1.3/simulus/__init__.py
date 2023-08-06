# FILE INFO ###################################################
# Author: Jason Liu <jasonxliu2010@gmail.com>
# Created on June 14, 2019
# Last Update: Time-stamp: <2019-07-10 14:00:21 liux>
###############################################################

"""Simulus is a discrete-event simulator in Python."""

from __future__ import absolute_import

import sys
if sys.version_info[:2] < (2, 8):
    raise ImportError("Simulus requires Python 2.8 and above (%d.%d detected)." %
                      sys.version_info[:2])
del sys

from .utils import *
from .trappable import *
from .trap import *
from .semaphore import *
from .resource import *
from .store import *
from .mailbox import *
from .simulator import *

__version__ = '1.1.3'
