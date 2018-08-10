from PyQt5.QtGui import *
from Model.transaction import *
from Model.asset_info import *
import math
import decimal
from Model.account_model import *
from Database.Account.transactions import *


class TransactionCtrl:
    def __init__(self, model, exchange):
        self.model = model
        self.exchange = exchange
        self.transactions = Transactions()


    def add_to_pending_list(self, item):
        if self.model.graphics_mode:
            index = self.model.pending_order_model.rowCount()
            item.pending_list_row = index
            self.model.pending_order_model.appendRow(QStandardItem(item.__str__()))
            item.status = "Pending"#Bad code, redesign!
           # self.transactions.update_transaction(item)


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
            item.status = "Active" #Bad code, redesign!
            self.transactions.update_transaction(item)

        self.model.data_writer_handler.update_transaction(transaction=item)  # update_transaction(transaction=item)
        #self.model.data_writer_handler.ping()



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
            item.status = "Closed" #Bad code, redesign!
           # self.transactions.update_transaction(item) #Move later to better palce.

    def rem_from_closed_list(self, item):
        if self.model.graphics_mode:
            if item.closed_list_row is not None:
                self.model.closed_order_model.removeRow(item.closed_list_row)
                item.closed_list_row = None

    def make_pending_transaction(self, item):
        item.status = "Pending"

        if self.model.graphics_mode:
            index = self.model.pending_order_model.rowCount()
            item.pending_list_row = index
            self.model.pending_order_model.appendRow(QStandardItem(item.__str__()))
        self.add_transaction(item)

    def paper_buy(self, item): #todo, check if balance is enough for purchase.
        price = self.exchange.get_price(item.target_currency + item.base_currency)
        price = float(price)
        item.quantity = self.calc_quantity(price, item)

        self.exchange.add_to_paper_balance(item.base_currency, -1 * (item.quantity * price))
        #balance = self.exchange.get_paper_balance(item.base_currency, -1 * (item.quantity * price))

        item.bought_at = float(price)
        item.active = True
        item.closed = False
        self.rem_from_pending_list(item)
        self.add_to_active_list(item)

        print("Paper Buy -> " + item.__str__())
        ts = time.time()
        dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #self.model.orders.insert_order(dateTime, item.target_currency + item.base_currency, "BUY", "", 0, item.quantity * price)
        file = open("Output.txt", "a")
        file.write("Paper Buy -> " + item.__str__() + "\n")
        file.close()

    def paper_sell(self, item):
        price = self.exchange.get_price(item.target_currency + item.base_currency)
        item.sold_at = float(price)
        self.exchange.add_to_paper_balance(item.base_currency, item.quantity * item.sold_at)
        self.model.close_transaction(item)
        item.active = False
        item.closed = True
        self.rem_from_active_list(item)
        self.add_to_closed_list(item)

        ts = time.time()
        dateTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.model.orders.insert_order(dateTime, item.target_currency + item.base_currency, "SEll", "", 0,
                                       item.quantity * item.sold_at)

        print("Paper Sell -> " + item.__str__())
        file = open("Output.txt", "a")
        file.write("Paper Sell -> " + item.__str__() + "\n")
        file.close()

    def calc_quantity(self, price, item):
        amount = item.amount / 100.0
        balance = float(self.exchange.get_paper_balance(item.base_currency, amount))
        q = (amount * balance) / price

        precision = item.asset_info.amount_min
        precision = self.nr_dec(precision)
        precision = abs(precision)

        format_str = "{0:." + str(precision) + "f}"

        q = float(format_str.format(q)) - 10.0 ** (-1 * precision )

        #q = self.round_down(q, int(item.asset_info.precision_amount))

        return q

    def load_transactions(self):
        print("Load Transactions")
        pending = self.transactions.get_all_transactions("Pending")
        active = self.transactions.get_all_transactions("Active")
        for p in pending:
            t_item = TransactionItem.gen_from_dict(p)
            d_data = self.model.asset_info.fetch_item("Binance", t_item.base_currency, t_item.target_currency)

            asset_info = AssetInfo("Binance", d_data)
            t_item.asset_info = asset_info
            self.model.transactions.append(t_item)
            self.add_to_correct_view(t_item)

        for a in active:
            t_item = TransactionItem.gen_from_dict(a)
            d_data = self.model.asset_info.fetch_item("Binance", t_item.base_currency, t_item.target_currency)
            asset_info = AssetInfo("Binance", d_data)
            t_item.asset_info = asset_info
            self.model.transactions.append(t_item)
            self.add_to_correct_view(t_item)

    def add_to_correct_view(self, t_item):
        if self.model.graphics_mode:
            if t_item.closed:
                self.add_to_closed_list(t_item)
            elif t_item.active:
                self.add_to_active_list(t_item)
            else:
                self.add_to_pending_list(t_item)

    def load_transactions2(self, transaction_list):
        for item in transaction_list: #todo: add logic to check previous version of transaction is already loaded.
            self.add_transaction(item)

            if self.model.graphics_mode:
                if item.closed:
                    self.add_to_closed_list(item)
                elif item.active:
                    self.add_to_active_list(item)
                else:
                    self.add_to_pending_list(item)

    def add_transaction(self, transaction):
        self.model.transactions.append(transaction)
      #  self.transactions.insert_transaction(transaction) #database

    def legal_transaction(self, transaction):
        price_precision = transaction.asset_info.precision_price
        price = round(transaction.buy_in, int(price_precision))
        balance = float(self.exchange.get_paper_balance(transaction.base_currency, 0))

        quantity = self.calc_quantity(price, transaction)

        if quantity > transaction.asset_info.amount_min and quantity < transaction.asset_info.amount_max:
            if quantity * price < balance:
                return True

        return False


    def round_down(self, num, precision):
        return (math.floor(num * (10**precision)) / (10.0 ** precision))

    def nr_dec(self, n):
        d = decimal.Decimal(str(n))
        return d.as_tuple().exponent










