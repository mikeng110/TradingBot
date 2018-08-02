import sqlite3

class Transactions: #rewrite to fit my transaction items, pending, active and closed.
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db')
        self.c = self.connection.cursor()

        self.c.execute('CREATE TABLE IF NOT EXISTS Transactions(Date text, Pair text, Type text, Filled text, Fee real, total real)')

        self.insert_transaction('Hello')
        self.read_from_db()
        self.close()

    def close(self):
        self.c.close()
        self.connection.close()

    def insert_transaction(self, transaction):
        pass
       # self.c.execute("INSERT INTO Transactions (date, pair, type, filled, fee, total) VALUES (?, ?, ?, ?, ?, ?)",
       #                (date, pair, type, filled, fee, total))
       # self.connection.commit()


    def read_from_db(self):
        self.c.execute('Select * From Transactions')
        for row in self.c.fetchall():
            print(row)