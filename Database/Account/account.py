import sqlite3

class Account:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db')
        self.c = self.connection.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS
            Balance
            (
                coin text,
                name text,
                total_balance real,
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

    def insert_balance(self, coin, name, total_balance, available_balance, locked_balance, btc_value):
        sql = """
        INSERT INTO 
            Balance
            (
                coin,
                name,
                total_balance,
                available_balance,
                locked_balance,
                btc_value
            ) 
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """
        self.c.execute(sql,
                       (coin, name, total_balance, available_balance, locked_balance, btc_value))
        self.connection.commit()

    def update_balance(self, coin, balance):
        sql = """
        UPDATE
            Balance
                SET
                    available_balance = ?
                WHERE coin = ?
            """
        self.c.execute(sql, (balance, coin))
        self.connection.commit()

    def read_from_db(self):
        self.c.execute('Select * From Balance')
        for row in self.c.fetchall():
            print(row)