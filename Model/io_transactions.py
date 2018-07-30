
class IoTransactions:
    def __init__(self, transactions):
        self.delimiter = ":"
        self.item_delimiter = "#"
        self.transactions = transactions
        pass

    '''
      self.pending_list_row = None
        self.active_list_row = None
        self.closed_list_row = None

        self.paper_trade = True

        self.active = False
        self.closed = False
        self.amount = amount
        self.buy_in = buy_in
        self.target = target
        self.stop_limit = stop_limit
        self.base_currency = base_currancy
        self.target_currency = target_currency

        self.bought_at = 0
        self.sold_at = 0
        self.quantity = 0
    
    '''

    def transaction_item_format(self, item):

        ret_str = ""

        ret_str += "paper_trade" + self.delimiter + str(item.paper_trade) + "\n"
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

    def export_t(self, file_name):
        file = open(file_name, 'w')
        data_str = ""
        for item in self.transactions:
            if not item.closed:
                data_str += self.transaction_item_format(item)
        file.write(data_str)
        file.close()

    def import_t(self, file_name):
        pass
