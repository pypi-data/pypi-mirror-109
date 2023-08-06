# -*- coding: utf-8 -*-

from pyodbc import connect, Connection, Cursor, Row

from monkey.crawler.crawler import Crawler
from monkey.crawler.processor import Processor


class PyODBCCrawler(Crawler):

    def __init__(self, source_name: str, processor: Processor, connection_str: str, sql_statement: str,
                 field_names: list[str], offset: int = 0, max_retry: int = 0):
        """Instantiates a crawler on an ODBC data source
        :param source_name: the name of the data source
        :param processor: the processor that will process every records
        :param connection_str: the string that defines how to connect the ODBC data source
        :param sql_statement: the SQL "SELECT" statement used to get the records
        :param field_names: a list of names to used as field names on crawled records. They can differ from projected
        column names as the will be applied in regards of declaration order.
        :param offset: indicates if many records have to be skipped before starting to process the data (0 by default)
        :param max_retry: indicates how many time the processing can be retried when it raises a recoverable error
        """
        super().__init__(source_name, processor, offset, max_retry)
        self.connection_str = connection_str
        self.sql_statement = sql_statement
        self.field_names = field_names
        self._connection: Connection
        self._cursor: Cursor

    def _get_records(self):
        self._connection = connect(self.connection_str)
        self.cursor = self._connection.cursor()
        self.cursor.execute(self.sql_statement).skip(self.offset)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            row: Row = self.cursor.__next__()
            return dict(zip(self.field_names, row))
        except StopIteration as e:
            raise e

    def _echo_start(self):
        self.logger.info(
            f'Crawling {self.source_name} from ODBC data source {self.connection_str}.'
        )
