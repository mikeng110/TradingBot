import threading
import sqlite3


class DatabaseManager:
    def __init__(self, db):
        self.db = db

    def __enter__(self):
        (conn, c) = self.db.connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.rem_connection()

    def connection(self):
        return self.db.connection()

    def execute(self, statement, sub_val=()):
        ret_val = None
        (conn, c) = self.db.connection()

        ret_val = c.execute(statement, sub_val)
        return ret_val

    def query(self, statement, sub_val=()):
        ret_val = None
        (conn, c) = self.db.connection()

        c.execute(statement, sub_val)
        ret_val = c.fetchall()
        conn.commit()

        return ret_val


class Database:
    def __init__(self, path, timeout=5.0):
        self.path = path
        self.timeout = timeout
        self.lock = threading.Lock()
        self._connections = {}

    def connection(self):
        self.lock.acquire()
        conn = self._connection()
        c = conn.cursor()
        self.lock.release()
        return conn, c

    def rem_connection(self):
        self.lock.acquire()
        self._rem_connection()
        self.lock.release()

    def _rem_connection(self):
        thread_id = threading.current_thread().ident
        if thread_id in self._connections:
            conn = self._connections[thread_id]
            c = conn.cursor()

            c.close()
            conn.close()
            del self._connections[thread_id]

    def _connection(self):
        thread_id = threading.current_thread().ident
        if thread_id in self._connections:
            return self._connections[thread_id]
        else:
            conn = self._create_connection()
            self._connections[thread_id] = conn
            return self._connections[thread_id]

    def _create_connection(self):
        conn = sqlite3.connect(self.path, timeout=self.timeout)
        return conn