# -*- coding: utf-8 -*-
"""Helps you to setup your repricer."""
import pandas as pd
from time import sleep
import mws

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


def auto_get_report_id(request, rec_level=0):
    """Takes the response from request_report and returns a reportid"""
    assert request.parsed.ReportRequestInfo.ReportProcessingStatus == '_SUBMITTED_'
    report_api = mws.apis.Reports(**mwscred)
    request_id = request.parsed.ReportRequestInfo.ReportRequestId

    sleep(120)
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
