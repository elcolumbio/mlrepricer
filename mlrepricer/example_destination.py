# -*- coding: utf-8 -*-
from sqlalchemy import types
from sqlalchemy import create_engine

from .. import setup


class AzureSQL:
    """
    For each data destination like MSSQL define your own ParentClass.

    You can even leverage another metaclass like we do here with
    sqlalchemy.types.
    """

    def __init__(self):
        # dtypes
        self._textshort = types.NVARCHAR(length=40)
        self._textmiddle = types.NVARCHAR(length=400)
        self._textlong = types.NVARCHAR(length=4000)  # NVARCH4000 is max
        self._floaty = types.Float
        self._inty = types.INTEGER
        self._datey = types.DATE
        self._datetimey = types.DATETIME
        self._timey = types.TIME
        self._booly = types.BINARY

        # connection data, pls change it
        self._conn_data = setup.configs()['AzureSQL']

    @property
    def conn(self):
        pymssqltext = 'mssql+pymssql://{}@{}:{}@{}:{}/{}'.format(
            self._conn_data['username'],
            self._conn_data['hostname'],
            self._conn_data['password'],
            self._conn_data['host'],
            self._conn_data['port'],
            self._conn_data['database'])
        return create_engine(pymssqltext)

    @property
    def dtypes(self):
        return dict(zip(self.mapping.keys(), [item[0] for item in list(
            self.mapping.values())]))

    @property
    def nullable(self):
        return dict(zip(self.mapping.keys(), [item[1] for item in list(
            self.mapping.values())]))
