#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import mws
from mws.apis.reports import ReportType
import numpy as np
import pandas as pd
import threading

from . import helper


class AsintoSku(threading.Thread):
    """Run once a day to asintosku our asins to skus."""

    def run(self):
        print(f'Starting {self.name}, this may take 2 mins')
        report = get_report(ReportType.ACTIVE_LISTINGS.value)
        # store the report
        reorganize(deduplicate(read_filter(report)))
        print(f'Exiting {self.name}')


def get_report(report_name):
    """Call reports easy."""
    report_api = mws.apis.Reports(**helper.mwscred)
    request_response = report_api.request_report(report_name)
    report_id = helper.auto_get_report_id(request_response)
    if report_id:
        report = report_api.get_report(report_id).parsed
    return report


def read_filter(report):
    i = pd.read_csv(io.StringIO(report), sep='\t', decimal='.',
                    thousands=None, dayfirst=True)
    i = i[i.loc[:, 'item-condition'] == 11]
    d = i.loc[:, ['seller-sku', 'asin1', 'fulfillment-channel']]
    d['county'] = 1
    return d.groupby(['asin1', 'fulfillment-channel']).agg(
        {'seller-sku': 'first', 'county': 'count'})


def deduplicate(listingperasin):
    """Remove duplicates."""
    duplicates = listingperasin[listingperasin.loc[:, 'county'] > 1]
    if len(duplicates) >= 1:
        print(f'you may want to delete one listing per asin {duplicates}')

    # those we return
    return listingperasin[listingperasin.county == 1].reset_index()


def reorganize(nocollusion):
    """We do some final cleanup and reorganize columns."""
    # When fulfillment-channel is DEFAULT its seller fulfilled
    nocollusion['isprime'] = np.where(
        nocollusion['fulfillment-channel'] == 'DEFAULT', 0, 1)
    nocollusion.drop(['fulfillment-channel', 'county'], axis=1, inplace=True)
    nocollusion.rename(
        {'asin1': 'asin', 'seller-sku': 'seller_sku'}, axis=1, inplace=True)
    helper.dump_dataframe(nocollusion, 'asintosku')
