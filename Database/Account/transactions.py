import sqlite3
import sys


class Transactions: #rewrite to fit my transaction items, pending, active and closed.
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db', check_same_thread=False)
        self.c = self.connection.cursor()
        self.create_table()
        self.read_from_db()


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

    def destroy(self):
        print("Destroy all")
        self.c.execute("DROP TABLE IF EXISTS Transactions")
        self.connection.commit()

    def insert_transaction(self, transaction): #rewrite to reconize if entry already exist.
        paper_trade = self.bool_to_int(transaction.paper_trade)
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

    def transaction_exist(self, transaction):
        self.c.execute("SELECT * FROM Transactions WHERE uid=?", (transaction.uid,))
        data = self.c.fetchall()
        if data.__len__() == 0:
            return False
        return True

    def update_transaction(self, transaction):
        paper_trade = self.bool_to_int(transaction.paper_trade)
        if self.transaction_exist(transaction):
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
        ret_data = []
        self.c.execute("SELECT * FROM Transactions WHERE status=?", (status,))
        data = self.c.fetchall()
        for e in data:
            ret_data.append(self.data_row_to_dict(e))

        return ret_data

    def data_row_to_dict(self, data):
        ret_data = {}
        col_names = self.get_column_names()

        if len(col_names) != len(data):
            return []
        for i, cn in enumerate(col_names):
                ret_data[cn] = data[i]

        return ret_data

    def get_column_names(self):
        data = []
        self.c.execute('select * from Transactions')
        for e in self.c.description:
            data.append(e[0])

        return data


    def read_from_db(self):
        self.c.execute('Select * From Transactions')
        for row in self.c.fetchall():
            print(row)

    def bool_to_int(self, b): #move to special library
        if b:
            return 1
        else:
            return 0