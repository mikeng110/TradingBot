import sqlite3

class DatabaseUpdate:
    def __init__(self):
        self.connection = sqlite3.connect('Database/Exchange.db', check_same_thread=False)
        self.c = self.connection.cursor()

        sql = """
                CREATE TABLE IF NOT EXISTS
                    Database_Update
                    (
                        exchange TEXT,
                        updated INTEGER
                    )
                    """

        self.c.execute(sql)
        self.connection.commit()

    def exchange_exist(self, exchange):
        self.c.execute("SELECT * FROM Database_Update WHERE exchange=?", (exchange,))
        data = self.c.fetchall()
        if data.__len__() == 0:
            return False
        return True

    def updated(self, exchange): #rewrite
        if self.exchange_exist(exchange):

            self.c.execute("SELECT updated FROM Database_Update WHERE exchange=?", (exchange,))
            data = self.c.fetchall()
            return bool(data[0])

        return


    def set_updated(self, exchange, updated):
        updated = self.bool_to_int(updated)
        sql = ""
        if self.exchange_exist(exchange):

            sql = """
                    UPDATE 
                        Database_Update 
                    SET 
                        updated=?
                           
                    WHERE 
                        exchange=?
                       """
        else:
            #self.c.execute("",
            sql ="""INSERT INTO Database_Update (exchange, updated) VALUES (?, ?)"""

        self.c.execute(sql, (exchange, updated))

        self.connection.commit()


    def bool_to_int(self, b):  # move to special library
        if b:
            return 1
        else:
            return 0
