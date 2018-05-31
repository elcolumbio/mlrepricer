#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mws
from mws.apis.reports import AllReports
from mlrepricer import setup
import pandas as pd
import io

mwscred = {
        'access_key': setup.configs['access_key'],
        'secret_key': setup.configs['secret_key'],
        'account_id': setup.configs['account_id'],
        'region': setup.configs['region']
    }


def get_report(report_name=AllReports.ACTIVE_LISTINGS.value):
    """Call reports easy."""
    report_api = mws.apis.Reports(**mwscred)
    request_response = report_api.request_report(report_name)
    report_id = report_api.get_reportid(request_response)
    if report_id:
        report = report_api.get_report(report_id).parsed
    # the result is a correct decoded string
    return report


def match(report):
    """Filter for new offers and nocollusion."""
    i = pd.read_csv(io.StringIO(report), sep='\t', decimal='.',
                    thousands=None, dayfirst=True)
    i = i[i.loc[:, 'item-condition'] == 11]
    d = i.loc[:, ['seller-sku', 'asin1', 'fulfillment-channel']]
    d['count'] = 1
    listingperasin = d.groupby(['asin1', 'fulfillment-channel']).agg(
        {'seller-sku': 'first', 'count': 'count'})

    # we ignore duplicates in our matching table
    duplicates = listingperasin[listingperasin.loc[:, 'count'] > 1]
    if len(duplicates) >= 1:
        print(f'you may want to delete one listing per asin {duplicates}')

    # those we return
    nocollusion = listingperasin[listingperasin.loc[:, 'count'] == 1]
    nocollusion.reset_index(level=['asin1'], inplace=True)
    nocollusion.reset_index(level=['fulfillment-channel'], inplace=True)
    return nocollusion
