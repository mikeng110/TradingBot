from Gui.MainGui import *
import time
import threading

from Bot.BotTrader import *

from Data.GuiModel import *


class Order:
    def __init__(self, gui, bot, amount, buy_in, target, stop_loss): #this is really bad design, figure out how to access data between classes, maybe sigelton pattern?

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

    def market_buy(self):
        price = self.gui.gui_data.current_price

        q = self.calculate_quantity(price, self.amount)
        print("Atempting to buy: " + str(q))
        if q > 0:
            try:
                self.bot.client.order_market_buy(symbol=self.symbol, quantity=q)
                print("Market order placed")
                self.quantity = q
                self.active = True
            except BinanceAPIException as e:
                self.quantity = 0
                self.active = False
                print("Market order Fail")
                print(e.status_code)
                print(e.message)
        else:
            print("quantity to low: " + str(q))

    def market_sell(self):
        if not self.active:
            print("Cant sold what you have not baught")
            return None

        print("Atempting to sell: " + str(self.quantity))
        if self.quantity > 0:
            try:
                self.bot.client.order_market_sell(symbol=self.symbol, quantity=self.quantity)
                print("Market sell order placed")
                self.active = False
                self.closed = True
            except BinanceAPIException as e:
                print("Market sell order Fail")
                print(e.status_code)
                print(e.message)
                self.active = True
        else:
            print("quantity to low: " + str(self.quantity))

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


class OrderList:
    def __init__(self):
        self.content = []

    def register_order(self, order):
        self.content.append(order)


class StartProgram:

    def __init__(self, app):
        app.aboutToQuit.connect(self.stop_threads)
        self.order_list = OrderList()
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

        print("Amount: " + str(amount) + " buy_in: " + str(buy_in) + " target: " + str(target) + " stop_loss: " + str(stop_loss))

        order = Order(self.gui, self.bot, amount, buy_in, target, stop_loss)
        order.symbol = self.gui_data.item + self.gui_data.currency
        self.order_list.register_order(order)

        if self.t2 is None:
            self.t2 = threading.Thread(target=self.price_watcher)
            self.t2.start()

    def price_watcher(self):

        while self.threads_running:
            for order in self.order_list.content:
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

            time.sleep(1)

    def stop_threads(self):
        print("Close threads")
        self.threads_running = False

        try:
            self.t1.join()
            self.t2.join()
        except Exception as e:
            return None

    def update_stats(self):

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
            time.sleep(1)