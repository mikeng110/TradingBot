from binance.client import Client
from binance.exceptions import *
import Gui
import time
import threading

#Test 2

class MainGuiData:
    def __init__(self):

        self.logged_in = False

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


class MainProgram:

    def __init__(self, app):
        app.aboutToQuit.connect(self.stop_threads)
        self.gui = Gui.MainWindow()
        self.temp_gui_data = MainGuiData() #Used for non applied values.
        self.gui_data = MainGuiData()
        self.lock = threading.Lock()

        self.gui.set_logged_in_mode(False)

        self.init_gui()

    def login(self):

        self.client = Client(self.gui.ui.Api_Key_tbx.text(), self.gui.ui.Api_Signature_tbx.text())
        try:
            self.client.get_account()
            self.gui_data.logged_in = True
            self.gui.ui.Login_Status_Display_lbl.setText("Status: Access Granted")

        except BinanceAPIException as e:
            print ("Wrong Api Key, or wrong Api Signature")
            self.gui.ui.Login_Status_Display_lbl.setText("Status: Access Denied")
            return None

        print (self.client.get_account())

        self.gui_data.logged_in = True
        self.gui.set_logged_in_mode(True)

        self.setup_combo()

        currency = self.gui.ui.Transaction_Currency_cbx.currentText()
        asset = self.gui.ui.Transaction_Symbol_cbx.currentText()


        current_price = self.get_current_price(asset + currency)
        self.gui.ui.Transaction_Buy_in_tbx.setText(str(current_price))

        self.threads_running = True
        self.t1 = threading.Thread(target=self.update_stats)
        self.t1.start()


    def get_all_asset_names(self):
        result = []
        account_info = self.client.get_account()
        banlist = []

        if account_info is None:
            return result

        for ai in account_info['balances']:
            if not ai['asset'].isdigit() and not ai['asset'] in banlist:
                result.append(ai['asset'])
        return result


    def get_current_balance(self, currency):
        result = None
        account_info = self.client.get_account()

        if account_info is None:
            return result

        for ai in account_info['balances']:
            if ai['asset'] == currency:
                result = ai['free']
                break
        return result


    def get_current_price(self, symbol):  # Loook into how to prevent getting to much data from the server.
        result = None
        ticker_stats = self.client.get_all_tickers()

        if ticker_stats is None:  # exit
            return result

        for ts in ticker_stats:
            if ts['symbol'] == symbol:
                result = ts['price']
                break
        return result


    def stop_threads(self):
        print("Close threads")
        self.threads_running = False

        try:
            self.t1.join()
        except Exception as e:
            return None


    def update_stats(self):
        self.gui_data.item = "EOS"
        self.gui_data.currency = "BTC"

        while self.threads_running:
            self.lock.acquire()
            self.gui_data.current_price = self.get_current_price(self.gui_data.item + self.gui_data.currency)
            self.gui_data.balance = self. get_current_balance(self.gui_data.currency)

            self.gui.ui.Transaction_Current_Price_Display_lbl.setText("Asset Price:  " + str(self.gui_data.current_price) + " " + self.gui_data.currency)
            self.gui.ui.Transaction_Account_Balance_Display_lbl.setText("Balance:       " + str(self.gui_data.balance) + " " + self.gui_data.currency)
            self.lock.release()
            time.sleep(1)


    def init_gui(self):

        self.gui.ui.Strategy_Target_Procent_hsr.sliderMoved.connect(self.slider_strategy_target)
        self.gui.ui.Strategy_Stop_Limit_Procent_hsr.sliderMoved.connect(self.slider_strategy_stop_limit)
        self.gui.ui.Transaction_Amount_Procent_Display_hsr.sliderMoved.connect(self.slider_transaction_amount)

        self.gui.ui.Strategy_Apply_btn.clicked.connect(self.strategy_apply)
        self.gui.ui.Login_Connect_btn.clicked.connect(self.login)

        self.gui.show()

    def setup_combo(self):
        asset_names = self.get_all_asset_names()
        self.gui.ui.Transaction_Currency_cbx.addItems(["BTC", "BNB", "ETH", "USDT"])

        self.gui.ui.Transaction_Symbol_cbx.addItems(asset_names)
        self.gui.ui.Transaction_Symbol_cbx.setCurrentIndex(1)

        self.gui.ui.Transaction_Currency_cbx.currentIndexChanged.connect(self.change_combo)
        self.gui.ui.Transaction_Symbol_cbx.currentIndexChanged.connect(self.change_combo)




    def change_combo(self):
        self.gui_data.currency = self.gui.ui.Transaction_Currency_cbx.currentText()
        self.gui_data.item = self.gui.ui.Transaction_Symbol_cbx.currentText()

        current_price = self.get_current_price(self.gui_data.item + self.gui_data.currency)
        if (current_price != None):
            self.gui.ui.Transaction_Buy_in_tbx.setText(str(current_price))
            self.gui.ui.Transaction_Status_Display_lbl.setText("Status:")
            self.gui.ui.Transaction_Execute_btn.setEnabled(True)
        else:
            self.gui.ui.Transaction_Status_Display_lbl.setText("Status: Item is not on the market in " + self.gui_data.currency)
            self.gui.ui.Transaction_Execute_btn.setEnabled(False)


    def slider_strategy_target(self, value):
        self.temp_gui_data.strategy_target = value
        self.gui.ui.Strategy_Target_Procent_Display_lbl.text = str(value) + "%"
        self.gui.ui.Strategy_Target_Procent_Display_lbl.setText(str(value) + "%")

    def slider_strategy_stop_limit(self, value):
        self.temp_gui_data.strategy_stop_limit = value
        self.gui.ui.Strategy_Stop_Limit_Procent_Display_lbl.setText(str(value) + "%")

    def slider_transaction_amount(self, value):
        self.temp_gui_data.transaction_amount = value
        self.gui.ui.Transaction_Amount_Procent_Display_lbl.setText(str(value) + "%")

    def strategy_apply(self):
        self.gui_data.strategy_target = self.temp_gui_data.strategy_target
        self.gui_data.strategy_stop_limit = self.temp_gui_data.strategy_stop_limit
        self.gui_data.transaction_amount = self.temp_gui_data.transaction_amount

        transaction_buy_in = self.str_to_float(self.gui.ui.Transaction_Buy_in_tbx.text())

        strategy_target = self.gui_data.strategy_target
        strategy_stop_limit = self.gui_data.strategy_stop_limit

        new_transaction_target = transaction_buy_in * (1 + strategy_target / 100.0)
        new_transaction_stop_limit = transaction_buy_in * (1 - strategy_stop_limit / 100.0)

        self.gui.ui.Transaction_Target_tbx.setText(str(new_transaction_target))
        self.gui.ui.Transaction_Stop_Limit_tbx.setText(str(new_transaction_stop_limit))

    def str_to_float(self, str):
        if str == "":
            return 0.0
        try:
            return float(str)
        except ValueError:
            print ("invalid format, expected decimal.")

    def otherDialog(self):
        self.gui = Gui.Window()
        self.gui.show()