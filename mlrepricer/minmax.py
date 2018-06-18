# -*- coding: utf-8 -*-
"""We start with some very primitive csv."""

import pandas as pd
from . import setup, helper

datafolder = setup.configs['datafolder']
filename = 'minmax.csv'


def load_csv():
    """We should reprice only skus with min max prices."""
    pd.read_csv('minmax.csv')


def dump_csv():
    """Present empty values first."""
    df = helper.load_dataframe('mapping')
    df['minPrice'] = None
    df['maxPrice'] = None
    dfold = pd.read_csv('minmax.csv')
    merged = dfold.append(df, ignore_index=True).groupby(
        'seller_sku').max().sort_values('maxPrice', na_position='first')
    merged.to_csv('minmax.csv', index=False)
