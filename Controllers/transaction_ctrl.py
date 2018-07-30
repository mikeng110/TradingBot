from PyQt5.QtGui import *


class TransactionCtrl:
    def __init__(self, model, exchange):
        self.model = model
        self.exchange = exchange

    def add_to_pending_list(self, item):
        if self.model.graphics_mode:
            index = self.model.pending_order_model.rowCount()
            item.pending_list_row = index
            self.model.pending_order_model.appendRow(QStandardItem(item.__str__()))

    def rem_from_pending_list(self, item):
        if self.model.graphics_mode:
            if item.pending_list_row is not None:
                self.model.pending_order_model.removeRow(item.pending_list_row)
                item.pending_list_row = None

    def add_to_active_list(self, item):
        if self.model.graphics_mode:
            index = self.model.active_order_model.rowCount()
            item.active_list_row = index
            self.model.active_order_model.appendRow(QStandardItem(item.__str__()))

    def rem_from_active_list(self, item):
        if self.model.graphics_mode:
            if item.active_list_row is not None:
                self.model.active_order_model.removeRow(item.active_list_row)
                item.active_list_row = None

    def add_to_closed_list(self, item):
        if self.model.graphics_mode:
            index = self.model.closed_order_model.rowCount()
            item.closed_list_row = index
            self.model.closed_order_model.appendRow(QStandardItem(item.__str__()))

    def rem_from_closed_list(self, item):
        if self.model.graphics_mode:
            if item.closed_list_row is not None:
                self.model.closed_order_model.removeRow(item.closed_list_row)
                item.closed_list_row = None

    def make_pending_transaction(self, item):
        self.model.transactions.append(item)

        if self.model.graphics_mode:
            index = self.model.pending_order_model.rowCount()
            item.pending_list_row = index
            self.model.pending_order_model.appendRow(QStandardItem(item.__str__()))

    def paper_buy(self, item): #todo, check if balance is enough for purchase.
        price = self.exchange.get_price(item.target_currency + item.base_currency)
        price = float(price)
        item.quantity = self.calc_quantity(price, item)
        self.exchange.add_to_paper_balance(item.base_currency, -1 * (item.quantity * price))
        item.bought_at = float(price)
        item.active = True
        self.rem_from_pending_list(item)
        self.add_to_active_list(item)

        print("Paper Buy -> " + item.__str__())

    def paper_sell(self, item):
        price = self.exchange.get_price(item.target_currency + item.base_currency)
        item.sold_at = float(price)
        self.exchange.add_to_paper_balance(item.base_currency, item.quantity * item.sold_at)
        item.closed = True
        item.active = False
        self.rem_from_active_list(item)
        self.add_to_closed_list(item)

        print("Paper Sell -> " + item.__str__())

    def calc_quantity(self, price, item):
        amount = item.amount / 100.0
        balance = float(self.exchange.get_paper_balance(item.base_currency))

        return (amount * balance) / price



