# -*- coding: utf-8 -*-

from pymongo.collection import Collection, ReturnDocument
from pymongo.database import Database
from pymongo.cursor import Cursor
from pymongo.errors import PyMongoError

from monkey.crawler.crawler import Crawler
from monkey.crawler.processor import Processor


class PyMongoCrawler(Crawler):

    def __init__(self, source_name: str, processor: Processor, connection_str: str, db_name: str, collection_name: str,
                 query_filter: str = None, projection=None, offset: int = 0, max_retry: int = 0, limit: int = 0,
                 sort=None):
        """Instantiates a crawler on an ODBC data source
        :param source_name: the name of the data source
        :param processor: the processor that will process every records
        :param connection_str: the string that defines how to connect the ODBC data source
        :param db_name:
        :param collection_name:
        :param query_filter: the SQL "SELECT" statement used to get the records
        :param offset: indicates if many records have to be skipped before starting to process the data (0 by default)
        :param max_retry: indicates how many time the processing can be retried when it raises a recoverable error
        """
        super().__init__(source_name, processor, offset, max_retry)
        self.db_name: str = db_name
        self.collection_name: str = collection_name
        self.connection_str: str = connection_str
        self.query_filter = query_filter
        self.projection = projection
        self.limit: int = limit
        self.sort = sort

    def _get_records(self):
        from pymongo import MongoClient
        self._connection = MongoClient(self.connection_str)
        self._database: Database = self._connection.get_database(self.db_name)
        self._collection: Collection = self._database[self.collection_name]
        self._cursor: Cursor = self._collection.find(filter=self.query_filter, projection=self.projection,
                                                     skip=self.offset, limit=self.limit, sort=self.sort)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._cursor.next()
        except StopIteration as e:
            raise e

    def _echo_start(self):
        self.logger.info(
            f'Crawling {self.source_name} from MongoDB data source {self.connection_str}.'
        )
