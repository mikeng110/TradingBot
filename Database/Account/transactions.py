from Database.database_manager import *
from Utils_Library.utils import *
from Utils_Library.database_util import *


class Transactions:
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
            Transactions
            (
                uid TEXT,
                date_time_active TEXT,
                date_time_closed TEXT,
                paper_trade INTEGER,
                status TEXT,
                buy_in REAL,
                target REAL,
                stop_limit REAL,
                base_currency TEXT,
                target_currency TEXT,
                bought_at REAL,
                sold_at REAL,
                quantity REAL
            )
            """
        print("Create transaction Table")
        self.db_manager.query(sql)

    def transaction_exist(self, transaction):
        for row in self.db_manager.query("SELECT uid FROM Transactions"):
            if row[0] == transaction.uid:
                return True
        else:
            return False

    def insert(self, transaction):
        if self.transaction_exist(transaction):
            return

        paper_trade = self.utils.bool_to_int(transaction.paper_trade)
        sql = """
        INSERT
            INTO 
                Transactions 
                (
                    uid,
                    date_time_active,
                    date_time_closed,
                    paper_trade,
                    status,
                    buy_in,
                    target,
                    stop_limit,
                    base_currency,
                    target_currency,
                    bought_at,
                    sold_at,
                    quantity
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
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """
        self.db_manager.query(sql, (transaction.uid, transaction.date_time_active, transaction.date_time_closed, paper_trade, transaction.status, transaction.buy_in, transaction.target,
                             transaction.stop_limit, transaction.base_currency, transaction.target_currency, transaction.bought_at,
                             transaction.sold_at, transaction.quantity))

    def update(self, transaction):
        self.insert(transaction)
        paper_trade = self.utils.bool_to_int(transaction.paper_trade)

        sql = """
            UPDATE 
                Transactions 
            SET 
                paper_trade=?,
                status=?,
                buy_in=?,
                target=?,
                stop_limit=?,
                base_currency=?,
                target_currency=?,
                bought_at=?,
                sold_at=?,
                quantity=?
            WHERE 
                uid=?
            """

        self.db_manager.query(sql, (paper_trade, transaction.status, transaction.buy_in, transaction.target,
                             transaction.stop_limit, transaction.base_currency, transaction.target_currency, transaction.bought_at,
                             transaction.sold_at, transaction.quantity, transaction.uid))

    def get_all_transactions(self, status):
        return self.get_all("status", status)

    def get_all(self, identifier_name, identifier_value):
        ret_data = []
        trans = "Transactions"

        sql = """
        SELECT * FROM """ + trans + """ 
            WHERE """ + identifier_name + """=?"""

        data = self.db_manager.query(sql, (identifier_value,))

        for e in data:
            ret_data.append(self.database_util.data_row_to_dict(e, self.get_column_names()))

        return ret_data

    def get_column_names(self):
        data = []

        sql = """SELECT * FROM Transactions"""

        d = self.db_manager.execute(sql)

        for e in d.description:
            data.append(e[0])

        return data