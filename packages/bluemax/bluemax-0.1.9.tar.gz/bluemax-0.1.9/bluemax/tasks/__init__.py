"""
    This is a our invoke program
"""
import os
import sys
import logging
from invoke import Program, Collection
from .sidney import sidney
from . import create
from . import run

VERSION = "0.1.9"

sys.path.insert(0, os.getcwd())

logging.basicConfig(level=logging.INFO)

_NAMESPACE_ = Collection()
try:
    from bluemax.sa import database

    _NAMESPACE_.add_collection(Collection.from_module(database))
except ImportError:
    pass
_NAMESPACE_.add_collection(Collection.from_module(create))
_NAMESPACE_.add_collection(Collection.from_module(run))
_NAMESPACE_.add_task(sidney)

program = Program(
    version=VERSION, namespace=_NAMESPACE_
)  # pylint: disable=C0103
