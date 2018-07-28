# -*- coding: utf-8 -*-
"""Entry point to run all parts of this packet."""

from .listener import Listener
from .asintosku import AsintoSku
from .updateprice import Updater


def runlistener():
    """You get a thread object run it with threadobject.start()."""
    return Listener()


def runmatch():
    """AsintoSku your skus to asins isprime combinations."""
    return AsintoSku()


def runupdater():
    """Run the demon to push price changes to your mws seller account."""
    return Updater()


def runminmax():
    """Still find out what is the best functionality."""
    pass
