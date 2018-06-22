# -*- coding: utf-8 -*-
"""Entry point to run all parts of this packet."""

from .listener import Listener
from .match import Match
from .updateprice import Updater


def runlistener():
    """You get a thread object run it with threadobject.start()."""
    return Listener()


def match():
    """Match your skus to asins isprime combinations."""
    return Match()


def updateprices():
    """Run the demon to push price changes to your mws seller account."""
    return Updater()
