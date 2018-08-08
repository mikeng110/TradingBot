from Utils_Library.database_util import *
from Utils_Library.utils import *


class Transactions: #rewrite to fit my transaction items, pending, active and closed.
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db', check_same_thread=False)
        self.c = self.connection.cursor()
        self.create_table()
        self.database_util = DatabaseUtil("Transactions", self.connection, self.c)
        self.utils = Utils()

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
        self.c.execute(sql)

    def close(self):
        self.c.close()
        self.connection.close()
        print("Closed Transaction TradingBot.db")

    def destroy(self):
        print("Destroy all")
        self.c.execute("DROP TABLE IF EXISTS Transactions")
        self.connection.commit()

    def insert_transaction(self, transaction):
        if self.database_util.item_exist("uid", transaction.uid):
            self.update_transaction(transaction)
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
        self.c.execute(sql, (transaction.uid, transaction.date_time_active, transaction.date_time_closed, paper_trade, transaction.status, transaction.buy_in, transaction.target,
                             transaction.stop_limit, transaction.base_currency, transaction.target_currency, transaction.bought_at,
                             transaction.sold_at, transaction.quantity))

        self.connection.commit()

    def update_transaction(self, transaction):
        paper_trade = self.utils.bool_to_int(transaction.paper_trade)
        if self.database_util.item_exist("uid", transaction.uid):
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
            self.c.execute(sql, (paper_trade, transaction.status, transaction.buy_in, transaction.target,
                                 transaction.stop_limit, transaction.base_currency, transaction.target_currency, transaction.bought_at,
                                 transaction.sold_at, transaction.quantity, transaction.uid))

            self.connection.commit()

    def get_all_transactions(self, status):
        return self.database_util.get_all("status", status)