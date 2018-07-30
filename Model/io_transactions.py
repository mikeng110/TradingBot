from Model.transaction import *
import fractions


class IoTransactions:
    def __init__(self, transactions):
        self.delimiter = ":"
        self.item_delimiter = "#"
        self.transactions = transactions

    def transaction_item_format(self, item):
        ret_str = ""

        ret_str += "paper_trade" + self.delimiter + str(item.paper_trade) + "\n"
        ret_str += "closed" + self.delimiter + str(item.closed) + "\n"
        ret_str += "active" + self.delimiter + str(item.active) + "\n"
        ret_str += "amount" + self.delimiter + str(item.amount) + "\n"
        ret_str += "buy_in" + self.delimiter + str(item.buy_in) + "\n"
        ret_str += "target" + self.delimiter + str(item.target) + "\n"
        ret_str += "stop_limit" + self.delimiter + str(item.stop_limit) + "\n"
        ret_str += "base_currency" + self.delimiter + str(item.base_currency) + "\n"
        ret_str += "target_currency" + self.delimiter + str(item.target_currency) + "\n"
        ret_str += "bought_at" + self.delimiter + str(item.bought_at) + "\n"
        ret_str += "sold_at" + self.delimiter + str(item.sold_at) + "\n"
        ret_str += "quantity" + self.delimiter + str(item.quantity) + "\n"
        ret_str += self.item_delimiter + "\n"

        return ret_str

    def convert_to_item(self, item_str):
        tokenzied = {}

        for str_line in item_str.split('\n'):
            tokenzied.update(self.tokenize(str_line))

        item = TransactionItem(tokenzied['amount'], tokenzied['buy_in'], tokenzied['target'], tokenzied['stop_limit'],
                               tokenzied['base_currency'], tokenzied['target_currency'])
        item.paper_trade = tokenzied['paper_trade']
        item.closed = tokenzied['closed']
        item.active = tokenzied['active']
        item.bought_at = tokenzied['bought_at']
        item.sold_at = tokenzied['sold_at']
        item.quantity = tokenzied['quantity']

        return item

    def tokenize(self, str_line):
        index = str_line.find(self.delimiter)
        key = str_line[:index]
        value = str_line[index+1:]

        if value == "True":
            value = True
        elif value == "False":
            value = False
        elif self.isnumber(value):
            value = float(value)

        return {key: value}

    def export_file(self, file_name):
        file = open(file_name, 'a')
        data_str = ""
        for item in self.transactions:
            if not item.closed:
                data_str += self.transaction_item_format(item)
        file.write(data_str)
        file.close()

    def import_file(self, file_name):
        transaction = []
        file = open(file_name, 'r')
        data_str = file.read()
        index = data_str.find(self.item_delimiter)

        while index != -1:
            item = self.convert_to_item(data_str[:index])
            data_str = data_str[:index]
            transaction.append(item)
            index = data_str.find(self.item_delimiter)

        file.close()

        return transaction

    def isnumber(self, s):
        try:
            float(s)
            return True
        except ValueError:
            try:
                fractions.Fraction(s)
                return True
            except ValueError:
                return False

