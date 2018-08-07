import sqlite3


class AssetInfo:
    def __init__(self):
        self.connection = sqlite3.connect('Database/Exchange.db',check_same_thread=False)
        self.c = self.connection.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS
            Asset_Info
            (
                exchange TEXT,
                base_currency TEXT,
                target_currency TEXT,
                amount_min REAL,
                amount_max REAL,
                precision_price REAL,
                precision_amount REAL,
                precision_base_currency REAL,
                precision_target_currency REAL
            )
            """
        self.c.execute(sql)
        #self.insert()

    def destroy(self):
        print("Destroy all")
        self.c.execute("DROP TABLE IF EXISTS Asset_Info")
        self.connection.commit()

    def close(self):
        self.c.close()
        self.connection.close()
        print("Closed Assets_Info Exchange.db")

    def insert(self, asset_info):
        sql = """
        INSERT INTO
            Asset_Info
            (
                exchange,
                base_currency,
                target_currency,
                amount_min,
                amount_max,
                precision_price,
                precision_amount,
                precision_base_currency,
                precision_target_currency
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
                ?
            )
            """



        self.c.execute(sql, (asset_info.exchange, asset_info.base_currency, asset_info.target_currency, asset_info.amount_min,
                             asset_info.amount_max, asset_info.precision_price, asset_info.precision_amount,
                             asset_info.precision_base_currency, asset_info.precision_target_currency))
        self.connection.commit()

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
        self.c.execute('select * from Asset_Info')
        for e in self.c.description:
            data.append(e[0])

        return data

    def fetch_item(self, exchange, base_currency, target_currency):
        self.c.execute("Select * From Asset_Info WHERE exchange=? AND base_currency=? AND target_currency=?", (exchange, base_currency, target_currency))
        data = self.c.fetchall()[0]

        return self.data_row_to_dict(data)

    def fetch(self, exchange):
        data = {}
        self.c.execute("Select * From Asset_Info WHERE exchange=?", (exchange,))
        for row in self.c.fetchall():
            pass

        return data

    def read_from_db(self):
        self.c.execute('Select * From Asset_Info')
        for row in self.c.fetchall():
            print(row)