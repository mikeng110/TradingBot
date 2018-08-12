import sqlite3


class DatabaseUtil:
    def __init__(self, table_name, connection, cursor):
        self.table_name = table_name
        self.connection = connection
        self.c = cursor

    def get_all(self, identifier_name, identifier_value):
        ret_data = []
        trans = "Transactions"

        sql = """
        SELECT * FROM """ + trans + """ 
            WHERE """ + identifier_name + """=?"""

        self.c.execute(sql, (identifier_value,))

        data = self.c.fetchall()
        for e in data:
            ret_data.append(self.data_row_to_dict(e))

        return ret_data

    def item_exist(self, identifier_name, identifier_value):
        sql = """
        SELECT * FROM """ + self.table_name + """ 
            WHERE """ + identifier_name + """=?"""

        self.c.execute(sql, (identifier_value,))
        data = self.c.fetchall()
        if data.__len__() == 0:
            return False
        return True

    def data_row_to_dict(self, data, col_names=None):
        ret_data = {}
        if col_names is None:
            col_names = self.get_column_names()

        if len(col_names) != len(data):
            return []
        for i, cn in enumerate(col_names):
            ret_data[cn] = data[i]

        return ret_data

    def get_column_names(self):
        data = []

        sql = """SELECT * FROM """ + self.table_name

        self.c.execute(sql)

        for e in self.c.description:
            data.append(e[0])

        return data