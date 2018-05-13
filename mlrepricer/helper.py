# -*- coding: utf-8 -*-
"""Helps you to setup your repricer."""
import pandas as pd

from . import setup

dataframefolder = f"{setup.configs['datafolder']}/alldata"

MARKETPLACES = {
    "CA": 'A2EUQ1WTGCTBG2',
    "US": 'ATVPDKIKX0DER',
    "DE": 'A1PA6795UKMFR9',
    "ES": 'A1RKKUPIHCS9HS',
    "FR": 'A13V1IB3VIYZZH',
    "IN": 'A21TJRUUN4KGV',
    "IT": 'APJ6JRA9NG5V4',
    "UK": 'A1F83G8C2ARO7P',
    "JP": 'A1VC38T7YXB528',
    "CN": 'AAHKV2X7AFYLW',
    "MX": 'A1AM78C64UM0Y8'}


def dump_dataframe(df):
    """Dump pandas df for storage."""
    with open(dataframefolder, 'wb') as f:
        df.to_msgpack(f)


def load_dataframe():
    """Load pandas df from storage."""
    with open(dataframefolder, 'rb') as f:
        return pd.read_msgpack(f)
