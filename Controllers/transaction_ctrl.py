from PyQt5.QtGui import *


class TransactionCtrl:
    def __init__(self, model):
        self.model = model

    def add_to_pending_list(self, item):

        index = self.model.pending_order_model.rowCount()
        item.pending_list_row = index
        self.model.pending_order_model.appendRow(QStandardItem(item.__str__()))

    def rem_from_pending_list(self, item):
        if item.pending_list_row is not None:
            self.model.pending_order_model.removeRow(item.pending_list_row)
            item.pending_list_row = None

    def add_to_active_list(self, item):
        index = self.model.active_order_model.rowCount()
        item.active_list_row = index
        self.model.active_order_model.appendRow(QStandardItem(item.__str__()))

    def rem_from_active_list(self, item):
        if item.active_list_row is not None:
            self.model.active_order_model.removeRow(item.active_list_row)
            item.active_list_row = None

    def make_pending_transaction(self, item):
        self.model.transactions.append(item)

        index = self.model.pending_order_model.rowCount()
        item.pending_list_row = index

        self.model.pending_order_model.appendRow(QStandardItem(item.__str__()))


