import sqlite3

class Orders:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db')
        self.c = self.connection.cursor()

        self.c.execute('CREATE TABLE IF NOT EXISTS Orders(Date text, Pair text, Type text, Filled text, Fee real, total real)')

        self.insert_order('Hello', '', '', '', 0.1, 100)
        self.read_from_db()
        self.close()

    def close(self):
        self.c.close()
        self.connection.close()

    def insert_order(self, date, pair, type, filled, fee, total):
        self.c.execute("INSERT INTO Orders (date, pair, type, filled, fee, total) VALUES (?, ?, ?, ?, ?, ?)",
                       (date, pair, type, filled, fee, total))
        self.connection.commit()


    def read_from_db(self):
        self.c.execute('Select * From Orders')
        for row in self.c.fetchall():
            print(row)