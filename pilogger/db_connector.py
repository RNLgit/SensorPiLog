import mysql.connector as sql
import os


class SQLLogger(object):
    READ_QUERY = "SELECT * FROM {table_name} {where_clause}"

    def __init__(self, host, port: 3306, user: str = None, password: str = None):
        self.host = host
        self.port = port
        self.user = user if user else os.environ.get("PI_SERVER_DB_USER")
        self.__password = password if password else os.environ.get("PI_SERVER_DB_PASSWORD")
        self.connection = None
        self.cursor = None

    def connect_database(self, database: str) -> None:
        if not self.connection.is_connected():
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

    def read_db_by_date(self, table_name: str, date: str) -> list:
        self.cursor.execute(self.READ_QUERY.format(table_name=table_name, where_clause=f"WHERE date = '{date}'"))
        return self.cursor.fetchall()
