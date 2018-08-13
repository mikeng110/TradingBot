from Database.database_manager import *
from Utils_Library.utils import *
from Utils_Library.database_util import *

class AssetInfoDB:
    def __init__(self, db):
        self.db = db
        self.utils = Utils()

        with DatabaseManager(db) as self.db_manager:
            self.create_table()
            (conn, c) = self.db_manager.connection()
            self.database_util = DatabaseUtil("Asset_Info", conn, c)

    def create_table(self):
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
        self.db_manager.query(sql)

    def clear(self, exchange):
        sql = """DELETE FROM Asset_Info WHERE exchange=?"""
        self.db_manager.query(sql, (exchange,))

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

        self.db_manager.query(sql, (asset_info.exchange, asset_info.base_currency, asset_info.target_currency, asset_info.amount_min,
                             asset_info.amount_max, asset_info.precision_price, asset_info.precision_amount,
                             asset_info.precision_base_currency, asset_info.precision_target_currency))

    def fetch_item(self, exchange, base_currency, target_currency):

        sql = """
            SELECT 
                *
            FROM 
                Asset_Info
            WHERE
                exchange=?
            AND
                base_currency=?
            AND
                target_currency=?
        """


        data = self.db_manager.query(sql, (exchange, base_currency, target_currency))

        return self.database_util.data_row_to_dict(data[0], self.get_column_names())

    def fetch(self, exchange):
        data = self.db_manager.query("Select * From Asset_Info WHERE exchange=?", (exchange,))

        return data

    def get_column_names(self):
        data = []

        sql = """SELECT * FROM Asset_Info"""

        d = self.db_manager.execute(sql)

        for e in d.description:
            data.append(e[0])

        return data
