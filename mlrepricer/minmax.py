# -*- coding: utf-8 -*-
"""We start with some very primitive csv."""

import pandas as pd
import numpy as np

from . import setup, helper

datafolder = setup.configs['datafolder']
filename = 'minmax.csv'
decimal = setup.decimal


def load_csv():
    """
    We should reprice only skus with min max prices.

    It is a userfile so we transform decimal to local.
    """
    df = pd.read_csv(datafolder+filename, decimal=decimal).astype(
        {'min': 'float', 'max': 'float'})
    return df


def dump_csv():
    """Merge old and new, then present empty values first."""
    df = helper.load_dataframe('mapping').reset_index()
    df['min'] = None
    df['max'] = None
    df.asin = df.asin + np.where(
        df.isprime == 0, '_seller', '_prime')
    del df['isprime']
    dfold = load_csv()
    merged = dfold.append(df, ignore_index=True, sort=True).sort_values(
        'min', ascending=False).drop_duplicates(['seller_sku'])
    merged[['asin', 'mean', 'min', 'max', 'seller_sku']].to_csv(
        datafolder+filename, index=False)
