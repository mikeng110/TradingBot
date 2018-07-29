from PyQt5.QtGui import *
class TransactionItem:
    def __init__(self, amount, buy_in, target, stop_limit, base_currancy, target_currency):
        self.pending_list_row = None
        self.active_list_row = None
        self.closed_list_row = None

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

    def __str__(self):
        ret_str = self.target_currency + self.base_currency + "\n|->"

        if self.active:
            ret_str += "Bought At: " + str(self.bought_at) + ", Target: " + str(self.target) + ", Stop Limit: " + str(self.stop_limit)

        elif self.closed:
            ret_str += "Bought At: " + str(self.bought_at) + ", Sold At: " + str(self.sold_at) + ", Profit: " + str(self.profit()) + "%"

        else:
            ret_str += "Buy In: " + str(self.bought_at) + ", Target: " + str(self.target) + ", Stop Limit: " + str(self.stop_limit)

        return ret_str

    def profit(self):
        return 0


