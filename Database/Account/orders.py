import sqlite3

class Orders:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db', check_same_thread=False)
        self.c = self.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS
            Orders
            (
                Date TEXT,
                Pair TEXT,
                Type TEXT,
                Filled TEXT,
                Fee REAL,
                total REAL
            )
        """
        self.c.execute(sql)

    def close(self):
        self.c.close()
        self.connection.close()
        print("Closed Orders TradingBot.db")

    def insert_order(self, date, pair, type, filled, fee, total):
        sql = """INSERT INTO 
            Orders
            (
                date,
                pair,
                type,
                filled,
                fee,
                total
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
                       (date, pair, type, filled, fee, total))
        self.connection.commit()