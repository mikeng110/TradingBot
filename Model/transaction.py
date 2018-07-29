from PyQt5.QtGui import *
class TransactionItem:
    def __init__(self, amount, buy_in, target, stop_limit, base_currancy, target_currency):
        self.pending_list_row = None
        self.active_list_row = None

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
        return "Buy in: " + str(self.buy_in)

    @staticmethod
    def statistic(self):
        return "statistic about the transaction"


