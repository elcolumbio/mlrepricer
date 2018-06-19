# -*- coding: utf-8 -*-
"""Helps you to setup your repricer."""
import pandas as pd
from time import sleep
import mws
import numpy as np

from . import setup

datafolder = setup.configs['datafolder']

mwscred = {
    'access_key': setup.configs['access_key'],
    'secret_key': setup.configs['secret_key'],
    'account_id': setup.configs['account_id'],
    'region': setup.configs['region']}

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


def dump_dataframe(df, foldername):
    """Dump pandas df for storage."""
    with open(datafolder+foldername, 'wb') as f:
        df.to_msgpack(f)


def load_dataframe(foldername):
    """Load pandas df from storage."""
    with open(datafolder+foldername, 'rb') as f:
        return pd.read_msgpack(f)


def cleanup(df):
    """Input the complete data and remove very bad listings in the output."""
    # we should calculate the winners we dropped.
    f1 = df[(df.instock == 1) & (df.isfeaturedmerchant == 1)]
    f1 = f1.drop(['instock', 'isfeaturedmerchant'], axis=1)
    # those offers suck too
    f1 = f1[(f1.shipping_maxhours+f1.shipping_minhours) <= 72]
    f1 = f1[(f1.feedback > 20) | (f1.isprime == 1)]
    return f1


def normalize(f1):
    """Take output from cleanup and scales and merge data."""
    # normalize the feedback count to a number between 0 and 1
    f1['feedback'] = np.where(np.log(f1.feedback+1)/10 <= 1,
                              np.log(f1.feedback+1)/10, 1)
    # normalize the feedbackpercent to a number between 0 and 1
    f1['feedbackpercent'] = (f1.feedbackpercent/100)**2
    # combine max and minshipping time to a number between 0 and 1
    f1['shipping_time'] = (f1.shipping_maxhours+f1.shipping_minhours)
    # one hot encode shipping time, there should be only 3-10 unique times
    f1 = pd.get_dummies(f1, prefix='shipping_time', columns=['shipping_time'])
    f1 = f1.drop(['shipping_maxhours', 'shipping_minhours'], axis=1)
    # linear transformation of none prime prices
    f1['price'] = np.where((f1.isprime == 0), f1.price*0.859-0.567, f1.price)
    f1 = f1.drop(['isprime'], axis=1)
    return f1


def auto_get_report_id(request, rec_level=0):
    """Takes the response from request_report and returns a reportid"""
    assert request.parsed.ReportRequestInfo.ReportProcessingStatus == '_SUBMITTED_'
    report_api = mws.apis.Reports(**mwscred)
    request_id = request.parsed.ReportRequestInfo.ReportRequestId

    sleep(60)
    statusdict = report_api.get_report_request_list(request_ids=request_id).parsed
    status = statusdict.ReportRequestInfo.ReportProcessingStatus

    if rec_level > 2:
        raise RuntimeError('After 360 Seconds your report wasnot completed')

    if status == '_SUBMITTED_' or status == '_IN_PROGRESS_':
        sleep(120)
        rec_level += 1
        return report_api.get_reportid(request, rec_level)
    elif status == '_DONE_':
        return statusdict.ReportRequestInfo.GeneratedReportId
    elif status == '_DONE_NO_DATA_':
        return ''
    else:
        raise ValueError('your reportrequestid is screwed: {}'.format(statusdict))
