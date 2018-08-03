import datetime
import time
import uuid


class TransactionItem:

    @property
    def closed(self):
        return self.__closed

    @closed.setter
    def closed(self, value):
        self.__closed = value
        self.date_time_closed = self.date_time_stamp() #rewrite this.

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        self.__active = value
        self.date_time_active = self.date_time_stamp()

    def __init__(self, amount, buy_in, target, stop_limit, base_currancy, target_currency):
        self.uid = str(uuid.uuid1())     #used in database
        self.pending_list_row = None
        self.active_list_row = None
        self.closed_list_row = None

        self.date_time_active = None
        self.date_time_closed = None

        self.paper_trade = True

        self.status = ""

        self.__active = False
        self.__closed = False
        self.amount = amount
        self.buy_in = buy_in
        self.target = target
        self.stop_limit = stop_limit
        self.base_currency = base_currancy
        self.target_currency = target_currency

        self.bought_at = 0
        self.sold_at = 0
        self.quantity = 0

    def date_time_stamp(self):
        ts = time.time()
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        ret_str = ""
        if self.paper_trade:
            ret_str = "Paper Trade -> "

        ret_str += self.target_currency + self.base_currency + "\n |_"

        if self.active:
            ret_str += "Timestamp: " + str(self.date_time_active) + ", Bought At: " + str(self.bought_at) + ", Target: " + str(self.target) + ", Stop Limit: " + str(self.stop_limit)

        elif self.closed:
            ret_str += "Timestamp: " + str(self.date_time_closed) + ", Bought At: " + str(self.bought_at) + ", Sold At: " + str(self.sold_at) + ", Profit: " + str(self.profit()) + "%"

        else:
            ret_str += "Buy In: " + str(self.buy_in) + ", Target: " + str(self.target) + ", Stop Limit: " + str(self.stop_limit)

        return ret_str

    @staticmethod
    def gen_from_dict(data):
        if data is None:
            return None
        ret_item = TransactionItem(None, None, None, None, None, None)
        ret_item.uid = data['uid']
        ret_item.date_time_active = data['date_time_active']
        ret_item.date_time_closed = data['date_time_closed']
        ret_item.paper_trade = bool(data['paper_trade'])
        ret_item.status = data['status']
        if ret_item.status == "Pending":
            ret_item.active = False
            ret_item.closed = False
        elif ret_item.status == "Active":
            ret_item.active = True
            ret_item.closed = False
        elif ret_item.status == "Closed":
            ret_item.active = False
            ret_item.closed = True

        ret_item.amount = 0 #implement proper later

        ret_item.buy_in = data['buy_in']
        ret_item.target = data['target']
        ret_item.stop_limit = data['stop_limit']
        ret_item.base_currency = data['base_currency']
        ret_item.target_currency = data['target_currency']
        ret_item.bought_at = data['bought_at']
        ret_item.sold_at = data['sold_at']
        ret_item.quantity = data['quantity']
        return ret_item

    def profit(self):
        if self.buy_in == 0:
            return 0

        return ((self.sold_at / self.buy_in) - 1) * 100


