# -*- coding: utf-8 -*-
"""Pushing new prices to amazon with the mws python api."""
import pandas as pd

from . import setup

access_key = setup.configs['access_key']
secret_key = setup.configs['secret_key']
account_id = setup.configs['account_id']
region = setup.configs['region']
