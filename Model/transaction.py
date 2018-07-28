class TransactionItem:
    def __init__(self, amount, buy_in, target, stop_limit, base_currancy, target_currency):
        self.id = "" #generate unique id
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

    @staticmethod
    def statistic(self):
        return "statistic about the transaction"



