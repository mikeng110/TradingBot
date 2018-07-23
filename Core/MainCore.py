from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Gui.MainGui import *
import time
import threading

from Bot.BotTrader import *

from Data.GuiModel import *


class Order:
    def __init__(self, gui, bot, amount, buy_in, target, stop_loss): #this is really bad design, figure out how to access data between classes, maybe sigelton pattern?
        self.order_id = 0
        self.buy_order_info = None
        self.sell_order_info = None
        self.pending_order_index = None #temp solutions, to find it in the model
        self.active_order_index = None

        self.gui = gui #redesign later
        self.bot = bot
        self.active = False
        self.closed = False

        self.symbol = None
        self.quantity = 0

        self.amount = amount
        self.buy_in = buy_in
        self.target = target
        self.stop_loss = stop_loss

        self.purchased_at = 0
        self.sold_at = 0

    def __str__(self):
        ret_str = ""

        if self.closed and self.quantity == 0:
            pass
        elif self.active:
            ret_str = "\n   Bought At: " + str(self.purchased_at) + " \n   Quantaty: " + str(self.quantity) + "\n   Target: " + str(self.target) + " \n   Stop Loss: " + str(self.stop_loss) + "\n"
        else:
            ret_str = "\n   Buy In: " + str(self.buy_in) + " \n   Target: " + str(self.target) + " \n   Stop Loss: " + str(self.stop_loss) + "\n"

        return ret_str

    def market_buy(self):
        price = self.gui.gui_data.current_price

        q = self.calculate_quantity(price, self.amount)
        print("Atempting to buy: " + str(q))
        if q > 0:
            try:
                self.buy_order_info = self.bot.client.order_market_buy(symbol=self.symbol, quantity=q)
                print("Market order placed")
                self.quantity = q
                self.active = True
                self.gui.gui_data.update_order(self.order_id, self)
                if self.buy_order_info is not None:
                    fills = self.buy_order_info['fills']
                    fills = fills[0]
                    p_price = fills['price']
                    print("price sold: " + p_price)
                    self.quantity = self.gui.str_to_float(fills['qty'])
                    self.purchased_at = self.gui.str_to_float(p_price)
            except BinanceAPIException as e:
                self.quantity = 0
                self.active = False
                print("Market order Fail")
                print(e.status_code)
                print(e.message)
        else:
            print("quantity to low: " + str(q))
            self.active = False
            self.closed = True

    def market_sell(self):
        if not self.active:
            print("Cant sold what you have not baught")
            return None

        print("Atempting to sell: " + str(self.quantity))
        if self.quantity > 0:
            try:
                self.sell_order_info = self.bot.client.order_market_sell(symbol=self.symbol, quantity=self.quantity)
                print("Market sell order placed")
                self.active = False
                self.closed = True
                if self.sell_order_info is not None:
                    fills = self.sell_order_info['fills']
                    fills = fills[0]
                    p_price = fills['price']
                    print("price sold: " + p_price)
                    self.sold_at = self.gui.str_to_float(p_price)
                self.show_statistics()
            except BinanceAPIException as e:
                print("Market sell order Fail")
                print(e.status_code)
                print(e.message)
                self.active = True
        else:
            print("quantity to low: " + str(self.quantity))

    def show_statistics(self):
        print("Buying Price: " + str(self.purchased_at) + "\nSold at: " + str(self.sold_at) + "\n Gain: " + str((self.gui.str_to_float(self.sold_at / self.purchased_at) - 1 ) * 100.0 ))

    def calculate_quantity(self, price, amount):
        buy_fee = 0.1
        sell_fee = 0.1
        min_buy = 0.01
        procentage_fee = (buy_fee + sell_fee) / 100.0
        procentage_amount = amount / 100.0
        balance = self.gui.str_to_float(self.gui.gui_data.balance)
        capital = balance * (procentage_amount - procentage_fee)
        quantity = round((capital / price) - min_buy, self.num_decimals(min_buy))
        if quantity < min_buy:
            quantity = 0

        return quantity

    def num_decimals(self, n):
        str_n = str(n)
        return str_n[::-1].find('.')


class StartProgram:

    def __init__(self, app):
        app.aboutToQuit.connect(self.stop_threads)
        self.bot = None
        self.t1 = None
        self.t2 = None
        self.threads_running = None
        self.temp_gui_data = MainModel()  # Used for non applied values.
        self.gui_data = MainModel()
        self.gui = MainWindow(gui_data=self.gui_data, temp_gui_data=self.temp_gui_data)

        self.lock = threading.Lock()

        self.gui.set_logged_in_mode(False)

        self.init_gui()

    def login(self):

        self.bot = Bot(self.gui.ui.Api_Key_tbx.text(), self.gui.ui.Api_Signature_tbx.text())

        if self.bot.connected:
            self.login_procedure()
            self.gui.ui.Login_Status_Display_lbl.setText("Status: Access Granted")
        else:
            self.gui.ui.Login_Status_Display_lbl.setText("Status: Access Denied")

    def login_procedure(self):
        self.gui.gui_data.logged_in = True
        self.gui.set_logged_in_mode(True)

        self.gui.gui_data.ticker_stats = self.bot.get_all_tickers()
        self.gui.gui_data.account_info = self.bot.get_account_info()

        self.gui.setup_combo()

        currency = self.gui.ui.Transaction_Currency_cbx.currentText()
        asset = self.gui.ui.Transaction_Symbol_cbx.currentText()

        current_price = self.gui.gui_data.get_price(asset + currency)
        self.gui.ui.Transaction_Buy_in_tbx.setText(str(current_price))

        list = self.gui.ui.Pending_Orders_lbx
        model = QStandardItemModel(list)
        self.gui.gui_data.pending_orders_model = model

        list.setModel(model)

        list = self.gui.ui.Filed_Orders_lbx
        model = QStandardItemModel(list)
        self.gui.gui_data.active_orders_model = model
        list.setModel(model)


        list.selectionModel().currentChanged.connect(self.gui.showId)



        self.threads_running = True
        self.t1 = threading.Thread(target=self.update_stats)
        self.t1.start()

    def init_gui(self):
        self.gui.init_gui()

        self.gui.ui.Strategy_Apply_btn.clicked.connect(self.gui.strategy_apply)
        self.gui.ui.Login_Connect_btn.clicked.connect(self.login)
        self.gui.ui.Transaction_Execute_btn.clicked.connect(self.execute_transaction)

        self.gui.show()

    def execute_transaction(self):

        amount = self.gui.gui_data.transaction_amount
        buy_in = self.gui.gui_data.transaction_buy_in
        target = self.gui.gui_data.transaction_target
        stop_loss = self.gui.gui_data.transaction_stop_limit


        order = Order(self.gui, self.bot, amount, buy_in, target, stop_loss)
        order.symbol = self.gui_data.item + self.gui_data.currency

        self.gui.gui_data.add_order(order)


        if self.t2 is None:
            self.t2 = threading.Thread(target=self.price_watcher)
            self.t2.start()

    def price_watcher(self):
        order_list = self.gui.gui_data.order_list

        while self.threads_running:
            for order in order_list:
                if order.closed:
                    continue
                price = self.gui_data.current_price
                if order.active:
                    if price >= order.target:
                        print("Sell at target: " + str(price))
                        order.market_sell()

                    if price <= order.stop_loss:
                        print("Sell at stop loss: " + str(price))
                        order.market_sell()

                elif price <= order.buy_in and price > order.stop_loss:
                    order.market_buy()

            time.sleep(0.5)

    def stop_threads(self):
        print("Close threads")
        self.threads_running = False

        try:
            self.t1.join()
            self.t2.join()
        except Exception as e:
            return None

    def update_stats(self): #currently only work with 1 order at a time

        while self.threads_running:
            self.lock.acquire()
            self.gui.gui_data.ticker_stats = self.bot.get_all_tickers()
            self.gui.gui_data.account_info = self.bot.get_account_info()

            self.gui.gui_data.current_price = self.gui.gui_data.get_price(self.gui.gui_data.item + self.gui.gui_data.currency)
            self.gui.gui_data.current_price = self.gui.str_to_float(self.gui.gui_data.current_price)
            self.gui.gui_data.balance = self.gui.gui_data.get_balance(self.gui.gui_data.currency)

            self.gui.ui.Transaction_Current_Price_Display_lbl.setText("Asset Price:  " + str(self.gui.gui_data.current_price) + " " + self.gui.gui_data.currency)
            self.gui.ui.Transaction_Account_Balance_Display_lbl.setText("Balance:       " + str(self.gui.gui_data.balance) + " " + self.gui.gui_data.currency)
            self.lock.release()
            time.sleep(0.5)