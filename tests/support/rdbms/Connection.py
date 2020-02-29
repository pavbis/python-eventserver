import logging
import pg8000

from contextlib import contextmanager
from threading import Lock

logger = logging.getLogger(__name__)


class Connection:

    def __init__(self):
        self._lock = Lock()
        self._connection = None
        self._cursor_holder = None

    def set_conn_kwargs(self, conn_kwargs):
        self._conn_kwargs = conn_kwargs

    def get(self):
        with self._lock:
            if not self._connection:
                self._connection = pg8000.connect(**self._conn_kwargs)
                self._connection.autocommit = True
        return self._connection

    def cursor(self):
        if not self._cursor_holder or self._cursor_holder.closed or self._cursor_holder.connection.closed != 0:
            logger.info("establishing a new connection to the postgres cluster")
            self._cursor_holder = self.get()
        return self._cursor_holder

    def close(self):
        if self._connection:
            self._connection.close()
            logger.info("closed connection to the postgresql cluster")
        self._cursor_holder = self._connection = None


@contextmanager
def get_connection_cursor(**kwargs):
    with pg8000.connect(**kwargs) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            yield cur
