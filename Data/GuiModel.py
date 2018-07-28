from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class MainModel:
    def __init__(self):

        self.pending_orders_model = None
        self.active_orders_model = None
        self.pending_orders = {}
        self.active_orders = {}
        self.order_list = []

        self.logged_in = False

        self.symbol = ""

        self.item = ""
        self.currency = ""
        self.current_price = 0
        self.balance = 0

        self.strategy_target = 0
        self.strategy_stop_limit = 0

        self.transaction_amount = 0
        self.transaction_buy_in = 0
        self.transaction_target = 0
        self.transaction_stop_limit = 0

        self.ticker_stats = []
        self.account_info = []

        self.login_msg = "" #implement later.

    def add_order(self, order):
        order.order_id = len(self.order_list)
        self.order_list.append(order)
        self.add_pending_order(order)

    def add_pending_order(self, order): #think of a better way to generate unique id
        item = QStandardItem(order.__str__())
        model = self.pending_orders_model

        model.appendRow(item)
        order.pending_order_index = model.indexFromItem(item)
        self.pending_orders[order.order_id] = order

    def add_active_order(self, order):
        item = QStandardItem(order.__str__())
        model = self.active_orders_model

        model.appendRow(item)
        order.active_order_index = model.indexFromItem(item)
        self.active_orders[order.order_id] = order

        self.remove_pending_order(order)

    def close_order(self, order):
        self.remove_active_order(order)
        self.active_orders_model.appendRow(QStandardItem(order.__str__()))


    def remove_pending_order(self, order):
        print("Remove pending order!")

        model = self.pending_orders_model
        row = order.pending_order_index.row()
        model.removeRow(row)

    def remove_active_order(self, order):
        model = self.active_orders_model
        row = order.active_order_index.row()
        model.removeRow(row)

    def update_order(self, order_id, order):
        if len(self.order_list) <= order_id:
            return

        self.order_list[order_id] = order

        if order.active:
            self.add_active_order(order)
        elif not order.active and order.closed:
            self.close_order(order)
        else:
            self.add_pending_order(order)


    def get_price(self, symbol):
        result = None

        if self.ticker_stats is None:  # exit
            return result

        for ts in self.ticker_stats:
            if ts['symbol'] == symbol:
                result = ts['price']
                break
        return result

    def get_all_asset_names(self):
        result = []

        if self.account_info is None:
            return result

        for ai in self.account_info['balances']:
            if not ai['asset'].isdigit():
                result.append(ai['asset'])
        return result

    def get_balance(self, currency):
        result = None

        if self.account_info is None:
            return result

        for ai in self.account_info['balances']:
            if ai['asset'] == currency:
                result = ai['free']
                break

        return result
