#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mws
from mws.apis.reports import ReportType
import pandas as pd
import io
import threading
import numpy as np

from . import helper


class Match(threading.Thread):
    """Run once a day to match our asins to skus."""

    def run(self):
        print(f'Starting {self.name}')
        report = get_report(ReportType.ACTIVE_LISTINGS.value)
        match(report)
        print(f'Exiting {self.name}')


def get_report(report_name):
    """Call reports easy."""
    report_api = mws.apis.Reports(**helper.mwscred)
    request_response = report_api.request_report(report_name)
    report_id = helper.auto_get_report_id(request_response)
    if report_id:
        report = report_api.get_report(report_id).parsed
    return report


def match(report):
    """Filter for new offers and nocollusion."""
    i = pd.read_csv(io.StringIO(report), sep='\t', decimal='.',
                    thousands=None, dayfirst=True)
    i = i[i.loc[:, 'item-condition'] == 11]
    d = i.loc[:, ['seller-sku', 'asin1', 'fulfillment-channel']]
    d['county'] = 1
    listingperasin = d.groupby(['asin1', 'fulfillment-channel']).agg(
        {'seller-sku': 'first', 'county': 'count'})

    # we ignore duplicates in our matching table
    duplicates = listingperasin[listingperasin.loc[:, 'county'] > 1]
    if len(duplicates) >= 1:
        print(f'you may want to delete one listing per asin {duplicates}')

    # those we return
    nocollusion = listingperasin[listingperasin.county == 1].reset_index()

    # we do some final cleanup and reorganize columns
    # When fulfillment-channel is DEFAULT its seller fulfilled
    nocollusion['isprime'] = np.where(
        nocollusion['fulfillment-channel'] == 'DEFAULT', 0, 1)
    nocollusion.drop(['fulfillment-channel', 'count'], axis=1, inplace=True)
    nocollusion.rename(
        {'asin1': 'asin', 'seller-sku': 'seller_sku'}, axis=1, inplace=True)
    helper.dump_dataframe(nocollusion, 'mapping')
