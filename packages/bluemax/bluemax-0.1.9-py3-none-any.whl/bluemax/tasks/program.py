"""
    This is a our invoke program
"""
import os
import sys
import logging
from invoke import Program, Collection
import bluemax
from . import create
from . import run

sys.path.insert(0, os.getcwd())

logging.basicConfig(level=logging.DEBUG)

_NAMESPACE_ = Collection()
try:
    from bluemax.sa import database

    _NAMESPACE_.add_collection(Collection.from_module(database))
except ImportError:
    pass
_NAMESPACE_.add_collection(Collection.from_module(create))
_NAMESPACE_.add_collection(Collection.from_module(run))

program = Program(
    version=bluemax.VERSION, namespace=_NAMESPACE_
)  # pylint: disable=C0103
