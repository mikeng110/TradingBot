import sqlite3
from Utils_Library.database_util import *

class AssetInfoDB:
    def __init__(self):
        self.connection = sqlite3.connect('Database/Exchange.db',check_same_thread=False)
        self.c = self.connection.cursor()
        self.database_util = DatabaseUtil("Asset_Info", self.connection, self.c)

        sql = """
        CREATE TABLE IF NOT EXISTS
            Asset_Info
            (
                exchange TEXT,
                base_currency TEXT,
                target_currency TEXT,
                amount_min REAL,
                amount_max REAL,
                precision_price REAL,
                precision_amount REAL,
                precision_base_currency REAL,
                precision_target_currency REAL
            )
            """
        self.c.execute(sql)

    def destroy(self):
        print("Destroy all")
        self.c.execute("DROP TABLE IF EXISTS Asset_Info")
        self.connection.commit()

    def close(self):
        self.c.close()
        self.connection.close()
        print("Closed Assets_Info Exchange.db")

    def insert(self, asset_info):
        sql = """
        INSERT INTO
            Asset_Info
            (
                exchange,
                base_currency,
                target_currency,
                amount_min,
                amount_max,
                precision_price,
                precision_amount,
                precision_base_currency,
                precision_target_currency
            ) 
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """

        self.c.execute(sql, (asset_info.exchange, asset_info.base_currency, asset_info.target_currency, asset_info.amount_min,
                             asset_info.amount_max, asset_info.precision_price, asset_info.precision_amount,
                             asset_info.precision_base_currency, asset_info.precision_target_currency))
        self.connection.commit()

    def fetch_item(self, exchange, base_currency, target_currency):
        self.c.execute("Select * From Asset_Info WHERE exchange=? AND base_currency=? AND target_currency=?", (exchange, base_currency, target_currency))
        data = self.c.fetchall()[0]

        return self.database_util.data_row_to_dict(data)

    def fetch(self, exchange):
        data = {}
        self.c.execute("Select * From Asset_Info WHERE exchange=?", (exchange,))
        for row in self.c.fetchall():
            pass

        return data