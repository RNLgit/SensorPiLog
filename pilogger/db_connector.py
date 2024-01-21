import mysql.connector as sql
from collections import namedtuple
from typing import Union
import datetime
import os

COLUMN = namedtuple("Column", ["name", "type", "null", "key", "default", "extra"])


class SQLLogger(object):
    TABLE_QUERY = "SELECT * FROM {table_name} {where_clause}"
    ORDER_BY = "ORDER BY {column_name} DESC"
    LIMIT = "LIMIT {limit}"

    def __init__(self, host, database: str = None, port: int = 3306, user: str = None, password: str = None):
        self.host = host
        self.port = port
        self.user = user if user else os.environ.get("PI_SERVER_DB_USER")
        self.__password = password if password else os.environ.get("PI_SERVER_DB_PASSWORD")
        self.connection = None
        self.cursor = None
        self.database = database if database else os.environ.get("PI_SERVER_DATABASE", None)
        if database:  # if database is provided, connect to it
            self.connect_database(self.database)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect_database(self, database: str) -> None:
        if not self.connection or self.connection.is_connected():
            self.connection = sql.connect(
                host=self.host, port=self.port, user=self.user, password=self.__password, database=database
            )
            self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def reconnect(self, database: str) -> None:
        if self.connection.is_connected():
            self.close()
            self.connect_database(database)

    @property
    def list_tables(self) -> list:
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        return [table[0] for table in tables]

    def list_columns(self, table_name: str) -> list:
        self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        return [
            COLUMN(
                col_name,
                col_type,
                True if is_null == "Yes" else False,
                col_key if not col_key == "" else None,
                col_default,
                col_extra if not col_extra == "" else None,
            )
            for col_name, col_type, is_null, col_key, col_default, col_extra in self.cursor.fetchall()
        ]

    def read_by_date(self, table_name: str, date: Union[str]) -> list:
        """
        Read all records from a table by date. Date must be in the format of datatime.date or YYYY-MM-DD
        :param table_name: name of the table in database to read from
        :param date: date to read from format as datetime.date or YYYY-MM-DD
        """
        if isinstance(date, datetime.date):
            date = date.strftime("%Y-%m-%d")
        where_date_clause = "WHERE DATE(sample_date) = {date}".format(date=date)
        self.cursor.execute(self.READ_QUERY.format(table_name=table_name, where_clause=where_date_clause))
        return self.cursor.fetchall()
