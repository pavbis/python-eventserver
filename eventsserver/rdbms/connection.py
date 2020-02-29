import psycopg2
from eventsserver.rdbms.parser import config

from contextlib import contextmanager
from threading import Lock


class Connection(object):
    __DATABASE_INI_FILE = 'eventsserver/rdbms/database.ini'
    __SECTION = 'postgresql'

    def __init__(self):
        self._lock = Lock()
        self._connection = None
        self._cursor_holder = None
        self._conn_kwargs = config(self.__DATABASE_INI_FILE, self.__SECTION)

    def get(self):
        with self._lock:
            if not self._connection or self._connection.closed != 0:
                self._connection = psycopg2.connect(**self._conn_kwargs)
                self._connection.autocommit = True
                self.server_version = self._connection.server_version
        return self._connection

    def cursor(self):
        if not self._cursor_holder or self._cursor_holder.closed or self._cursor_holder.connection.closed != 0:
            self._cursor_holder = self.get().cursor()
        return self._cursor_holder

    def close(self):
        if self._connection and self._connection.closed == 0:
            self._connection.close()
        self._cursor_holder = self._connection = None


@contextmanager
def get_connection_cursor(**kwargs):
    with psycopg2.connect(**kwargs) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            yield cur
