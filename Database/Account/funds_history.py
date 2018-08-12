import sqlite3


class FundsHistoryDB:
    def __init__(self):
        self.connection = sqlite3.connect('TradingBot.db', check_same_thread=False, timeout=5)
        self.c = self.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS
            Funds_History
            (
                date TEXT,
                coin TEXT,
                amount REAL,
                information REAL
            )
        """
        self.c.execute(sql)

    def close(self):
        self.connection.commit()
        self.c.close()
        self.connection.close()
        print("Closed Orders TradingBot.db")

    def insert(self, date, coin, amount, information):
        sql = """INSERT INTO 
            Funds_History
            (
                date,
                coin,
                amount,
                information
            ) 
            VALUES 
            (
                ?,
                ?,
                ?,
                ?
            )
        """
        self.c.execute(sql,
                       (date, coin, amount, information))
        self.connection.commit()
