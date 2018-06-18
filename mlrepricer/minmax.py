# -*- coding: utf-8 -*-
"""We start with some very primitive csv."""

import pandas as pd
from . import setup, helper

datafolder = setup.configs['datafolder']
filename = 'minmax.csv'


def load_csv():
    """We should reprice only skus with min max prices."""
    return pd.read_csv(datafolder+filename)


def dump_csv():
    """Merge old and new, then present empty values first."""
    df = helper.load_dataframe('mapping')
    df['minPrice'] = None
    df['maxPrice'] = None
    dfold = load_csv()
    merged = dfold.append(df, ignore_index=True, sort=True).groupby(
        'seller_sku').max().sort_values('maxPrice', na_position='first')
    merged.to_csv(datafolder+filename)
