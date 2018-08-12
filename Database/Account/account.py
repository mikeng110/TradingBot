from Database.database_manager import *
from Utils_Library.database_util import *
from Utils_Library.utils import *


class AccountBalance:
    def __init__(self, db):
        self.db = db
        self.utils = Utils()

        with DatabaseManager(db) as self.db_manager:
            self.create_table()
            (conn, c) = self.db_manager.connection()
            self.database_util = DatabaseUtil("Balance", conn, c)

    def create_table(self):
        sql = """
               CREATE TABLE IF NOT EXISTS
                   Balance
                   (
                       coin text,
                       available_balance real,
                       locked_balance real,
                       btc_value real
                   ) 
                   """
        self.db_manager.query(sql)

    def update(self, coin, available_balance, locked_balance, btc_value):

        if not self.item_exist(coin):
            sql = """
            INSERT INTO 
                Balance
                (
                    coin,
                    available_balance,
                    locked_balance,
                    btc_value
                ) 
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?
                )
                """
            self.db_manager.query(sql, (coin, available_balance, locked_balance, btc_value))

        else:
            sql = """
                UPDATE 
                    Balance 
                SET 
                    available_balance = ?,
                    locked_balance = ?,
                    btc_value = ?
                WHERE 
                    coin=?
            """
            self.db_manager.query(sql, (available_balance, locked_balance, btc_value, coin))

    def get_all_balances(self):
        ret_data = []
        sql = """SELECT * FROM Balance"""
        data = self.db_manager.query(sql)
        for d in data:
            ret_data.append(self.database_util.data_row_to_dict(d, self.get_column_names()))

        return ret_data

    def item_exist(self, coin):
        sql = """SELECT * FROM Balance WHERE coin=?"""

        data = self.db_manager.query(sql, (coin,))
        if data.__len__() == 0:
            return False
        return True

    def get_column_names(self):
        data = []

        sql = """SELECT * FROM Balance"""

        d = self.db_manager.execute(sql)

        for e in d.description:
            data.append(e[0])

        return data
