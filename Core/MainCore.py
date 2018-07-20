from Gui.MainGui import *
import time
import threading

from Bot.BotTrader import *

from Data.GuiModel import *


class StartProgram:

    def __init__(self, app):
        app.aboutToQuit.connect(self.stop_threads)
        self.t1 = None
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
        self.gui.show()

    def stop_threads(self):
        print("Close threads")
        self.threads_running = False

        try:
            self.t1.join()
        except Exception as e:
            return None

    def update_stats(self):
        self.gui.gui_data.item = "EOS"
        self.gui.gui_data.currency = "BTC"

        while self.threads_running:
            self.lock.acquire()
            self.gui.gui_data.ticker_stats = self.bot.get_all_tickers()
            self.gui.gui_data.account_info = self.bot.get_account_info()

            self.gui.gui_data.current_price = self.gui.gui_data.get_price(self.gui.gui_data.item + self.gui.gui_data.currency)
            self.gui.gui_data.balance = self.gui.gui_data.get_balance(self.gui.gui_data.currency)

            self.gui.ui.Transaction_Current_Price_Display_lbl.setText("Asset Price:  " + str(self.gui.gui_data.current_price) + " " + self.gui.gui_data.currency)
            self.gui.ui.Transaction_Account_Balance_Display_lbl.setText("Balance:       " + str(self.gui.gui_data.balance) + " " + self.gui.gui_data.currency)
            self.lock.release()
            time.sleep(1)


