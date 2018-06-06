# -*- coding: utf-8 -*-
from sqlalchemy import types
from sqlalchemy import create_engine

from mlrepricer import setup


class AzureTarget():
    """
    For each data destination like MSSQL on Azure define your own ParentClass.
    """

    def __init__(self):
        # dtypes
        self.textshort = types.NVARCHAR(length=40)
        self.textmiddle = types.NVARCHAR(length=400)
        self.textlong = types.NVARCHAR(length=4000)  # 4000 is max for nvarchar
        self.floaty = types.Float
        self.inty = types.INTEGER
        self.datey = types.DATE
        self.datetimey = types.DATETIME
        self.timey = types.TIME
        self.booly = types.BINARY

        # connection data, pls change it in your setup yaml file
        self.conn_data = setup.configs['AzureSQL']

    def connection_engine(self):
        pymssqltext = 'mssql+pymssql://{}@{}:{}@{}:{}/{}'.format(
            self.conn_data['username'], self.conn_data['hostname'],
            self.conn_data['password'],
            self.conn_data['host'], self.conn_data['port'],
            self.database)
        return create_engine(pymssqltext)
