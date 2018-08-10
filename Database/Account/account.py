import sqlite3
from Utils_Library.database_util import *


class AccountBalance:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db', check_same_thread=False)
        self.c = self.connection.cursor()
        self.database_util = DatabaseUtil("Balance", self.connection, self.c)
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
        self.c.execute(sql)

    def close(self):
        self.c.close()
        self.connection.close()
        print("Closed Balance TradingBot.db")

    def update(self, coin, available_balance, locked_balance, btc_value):

        if not self.database_util.item_exist("coin", coin):
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
            self.c.execute(sql, (coin, available_balance, locked_balance, btc_value))
            self.connection.commit()
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
            self.c.execute(sql, (available_balance, locked_balance, btc_value, coin))
            self.connection.commit()


    def get_all_balances(self):
        ret_data = []
        sql = """SELECT * FROM Balance"""
        self.c.execute(sql)
        for data in self.c.fetchall():
            ret_data.append(self.database_util.data_row_to_dict(data))

        return ret_data
