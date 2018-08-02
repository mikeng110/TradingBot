import sqlite3

class Account:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db')
        self.c = self.connection.cursor()

        self.c.execute('CREATE TABLE IF NOT EXISTS Balance(coin text, name text, total_balance real, available_balance real, locked_balance real, btc_value real)')

        self.insert_balance('Hello', '', '', '', 0.1, 100)
        self.read_from_db()
       # self.close()

    def close(self):
        self.c.close()
        self.connection.close()

    def insert_balance(self, coin, name, total_balance, available_balance, locked_balance, btc_value):
        self.c.execute("INSERT INTO Balance (coin, name, total_balance, available_balance, locked_balance, btc_value) VALUES (?, ?, ?, ?, ?, ?)",
                       (coin, name, total_balance, available_balance, locked_balance, btc_value))
        self.connection.commit()

    def update_balance(self, coin, balance):
        self.c.execute("UPDATE Balance SET available_balance = ? WHERE coin = ?", (balance, coin))
        self.connection.commit()

    def read_from_db(self):
        self.c.execute('Select * From Balance')
        for row in self.c.fetchall():
            print(row)