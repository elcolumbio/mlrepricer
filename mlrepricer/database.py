# -*- coding: utf-8 - *-
"""
Abstracts your target from your table definitions target and you can use it.

Example how you inherit from it.
def saletaxdoo(target):
    class SaleTaxdoo(target):
        "A table definition."
        def __init__(self):
            super().__init__()
            self.table = 'taxdoo_sale'
        @property
        def mapping(self):
            return {'transaction_start_date': (self._datey, False)}

tableobject = saletaxdoo(AzureSQL)()  # AzureSQL is defined in this module

# create  empty table if needed, with all columns, autoid, notnull
metadata = MetaData(bind=tableobject.conn)
createtable = Table(
    tableobject.table, metadata,
    Column('ID', Integer, primary_key=True),
    *(Column(columnz, dtypez, nullable=nself.tableobject.nullable[columnz]
             ) for columnz, dtypez in tableobject.dtypes.items()))
if not createtable.exists():
    createtable.create()
"""

from sqlalchemy import types
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, MetaData


from . import setup


class SQLite:
    """
    Default local SQLite database.

    You can even leverage another metaclass like we do here with
    sqlalchemy.types.
    """

    def __init__(self):
        """Map the dtypes of your database to our definitions."""
        # if you have unicode it's best to use NVARCHAR
        self._textshort = types.NVARCHAR(length=40)
        self._textmiddle = types.NVARCHAR(length=400)
        self._textlong = types.NVARCHAR(length=4000)  # NVARCH4000 is max
        self._floaty = types.Float
        self._numericy = types.DECIMAL(10, 2)
        self._inty = types.INTEGER
        self._datey = types.DATE
        self._datetimey = types.DATETIME
        self._timey = types.TIME
        self._booly = types.BOOLEAN

        # Connection data, see the central config.yaml file.
        self._conn_data = setup.configs['SQLite']

    @property
    def conn(self):
        """Return a connection string you use like pandas.read_sql_table."""
        self.database = self._conn_data['database']
        return create_engine(
            f"sqlite:////{setup.configs['datafolder']}/{self.database}")

    @property
    def dtypes(self):
        """Use for creating tables, you have to implement mappings."""
        return dict(zip(self.mapping.keys(), [item[0] for item in list(
            self.mapping.values())]))

    @property
    def nullable(self):
        """Use for creating tables, you have to implement mappings."""
        return dict(zip(self.mapping.keys(), [item[1] for item in list(
            self.mapping.values())]))

    @property
    def createtable(self):
        """Create  empty table if needed, with all columns, autoid, notnull."""
        metadata = MetaData(bind=self.conn)

        tabletocreate = Table(
            self.table, metadata,
            Column('ID', Integer, primary_key=True),
            *(Column(columnz, dtypez, nullable=self.nullable[columnz]
                     ) for columnz, dtypez in self.dtypes.items()))
        if not tabletocreate.exists():
            tabletocreate.create()


class AzureSQL:
    """
    For each data destination like MSSQL define your own Class.

    This is an example for a client server database.
    """

    def __init__(self):
        """Map the dtypes of your database to our definitions."""
        # if you have unicode it's best to use NVARCHAR
        self._textshort = types.NVARCHAR(length=40)
        self._textmiddle = types.NVARCHAR(length=400)
        self._textlong = types.NVARCHAR(length=4000)  # NVARCH4000 is max
        self._floaty = types.Float
        self._inty = types.INTEGER
        self._datey = types.DATE
        self._datetimey = types.DATETIME
        self._timey = types.TIME
        self._booly = types.BOOLEAN

        # Connection data, see the central config.yaml file.
        self._conn_data = setup.configs['AzureSQL']

    @property
    def conn(self):
        """Return a connection string you use like pandas.read_sql_table."""
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
        """Use for creating tables, you have to implement mappings."""
        return dict(zip(self.mapping.keys(), [item[0] for item in list(
            self.mapping.values())]))

    @property
    def nullable(self):
        """Use for creating tables, you have to implement mappings."""
        return dict(zip(self.mapping.keys(), [item[1] for item in list(
            self.mapping.values())]))

    @property
    def createtable(self):
        """Create  empty table if needed, with all columns, autoid, notnull."""
        metadata = MetaData(bind=self.conn)

        tabletocreate = Table(
            self.table, metadata,
            Column('ID', Integer, primary_key=True),
            *(Column(columnz, dtypez, nullable=self.nullable[columnz]
                     ) for columnz, dtypez in self.dtypes.items()))
        if not tabletocreate.exists():
            tabletocreate.create()
