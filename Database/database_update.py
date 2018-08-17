from Database.database_manager import *
from Utils_Library.utils import *


class DatabaseUpdate:
    def __init__(self, db):
        self.db = db
        self.utils = Utils()

        with DatabaseManager(db) as self.db_manager:
            self.create_table()

    def create_table(self):
        sql = """
                CREATE TABLE IF NOT EXISTS
                    Database_Update
                    (
                        exchange TEXT,
                        updated INTEGER
                    )
                    """
        self.db_manager.query(sql)

    def exchange_exist(self, exchange):
        data = self.db_manager.query("SELECT * FROM Database_Update WHERE exchange=?", (exchange,))
        if data.__len__() == 0:
            return False
        return True

    def updated(self, exchange): #rewrite
        if self.exchange_exist(exchange):
            data = self.db_manager.query("SELECT updated FROM Database_Update WHERE exchange=?", (exchange,))
            flag = bool(data[0][0])
            return flag

        return False

    def set_updated(self, exchange, updated):
        updated = self.bool_to_int(updated)
        sql = ""
        if self.exchange_exist(exchange):
            sql = """
                    UPDATE 
                        Database_Update 
                    SET 
                        updated=?
                           
                    WHERE 
                        exchange=?
                       """
        else:
            sql ="""INSERT INTO Database_Update (updated, exchange) VALUES (?, ?)"""

        self.db_manager.query(sql, (updated, exchange))

    def get_updated(self):
        ret_data = []
        data = self.db_manager.query("SELECT exchange FROM Database_Update WHERE updated=1")
        for e in data:
            ret_data.append(e[0])

        return ret_data

    def bool_to_int(self, b):  # move to special library
        if b:
            return 1
        else:
            return 0
