from API.trading_broker import *
from Bot.fetcher_bot import *
from Bot.transaction_bot import *
from Model.transaction import *
from Controllers.transaction_ctrl import *
from Model.io_transactions import *
from Model.asset_info import *
from Database.database_update import *
import time


class MainController(object):

    def __init__(self, model, app=None):
        self.model = model
        self.exchange = Exchange(model)
        self.fetcher_bot = None
        self.transaction_bot = None
        self.app = app
        if self.app is not None:
            self.model.graphics_mode = True
        else:
            self.model.graphics_mode = False
        self.tc = TransactionCtrl(model, self.exchange)
       # print("Success")

    def change_login_api_key(self, value):
        self.model.login_api_key = value
        self.model.update_func("login_api_key")
       # print("Updated login_api_key " + str(value))

    def change_login_api_sign(self, value):
        self.model.login_api_sign = value
        self.model.update_func("login_api_sign")
       # print("Updated login_login_api_sign " + str(value))

    def change_strategy_target(self, value):

        self.model.strategy_target = value / self.model.strategy_slider_weight
        self.model.update_func("strategy_target")
      #  print("Updated strategy_target " + str(self.model.strategy_target))

    def change_strategy_stop_limit(self, value):
        self.model.strategy_stop_limit = value / self.model.strategy_slider_weight
        self.model.update_func("strategy_stop_limit")
     #   print("Updated strategy_stop_limit " + str(self.model.strategy_target))

    def change_strategy_sliders_weight(self, value):
        self.model.strategy_slider_weight = value

    def change_paper_trade_status(self, value):
        self.model.paper_trade_status = value
        if value:
            self.paper_login()

    def change_transaction_amount(self, value):
        self.model.transaction_amount = value
        self.model.update_func("transaction_amount")
     #   print("transaction_amount " + str(value))

    def change_transaction_buy_in(self, value):
        self.model.transaction_buy_in = value
        self.model.update_func("transaction_buy_in")
     #   print("Updated transaction buy in " + str(value))

    def change_transaction_target(self, value):
        self.model.transaction_target = value
        self.model.update_func("transaction_target")
     #   print("Updated transaction target " + str(value))

    def change_transaction_stop_limit(self, value):
        self.model.transaction_stop_limit = value
        self.model.update_func("transaction_stop_limit")
     #   print("Updated transaction_stop_limit " + str(value))

    def change_base_currency(self, value):
        self.model.base_currency = value
        self.model.target_currency_data = self.model.currency_data[value]

        if self.model.base_currency != '' and self.model.target_currency != '':  # rewrite so this is not needed
            d_data = self.model.asset_info.fetch_item("Binance", self.model.base_currency, self.model.target_currency)
            self.model.current_asset_info = AssetInfo("Binance", d_data)
            time.sleep(0.5)

        self.model.update_func("target_currency_options")


     #   print("Updated base currency: " + str(value))

    def change_target_currency(self, value):
        self.model.target_currency = value

        if self.model.base_currency != '' and self.model.target_currency != '': #rewrite so this is not needed
            d_data = self.model.asset_info.fetch_item("Binance", self.model.base_currency, self.model.target_currency)
            self.model.current_asset_info = AssetInfo("Binance", d_data)
            time.sleep(0.5)

     #   print("Updated target currency: " + str(value))

    def change_account_balance(self, value):
        self.model.account_balance = value
        self.model.update_func("account_balance")
    #    print("account_balance " + str(value))

    def import_transactions(self):
        io = IoTransactions(self.model.transactions)
        t_list = io.import_file("Exported.txt")
        #self.tc.load_transactions(t_list)

    def export_transactions(self):
        io = IoTransactions(self.model.transactions)
        io.export_file("Exported.txt")


    def paper_login(self):
        self.model.base_currency = "BTC"
        self.model.target_currency = "ETH"
        (free, locked) = self.model.account_balance_db.get_balance(self.model.base_currency)
        self.model.paper_account_balance = free
        self.login_procedure()

    def login(self):
        key = self.model.login_api_key
        sign = self.model.login_api_sign

        self.exchange.connect(key, sign)

        if self.exchange.connection_active:
            self.model.login_msg = "Login Success"
            self.login_procedure()
        else:
            self.model.login_msg = "Login Fail"

    def login_procedure(self):
        self.model.logged_in = True
        self.model.init_data()
        #self.model.transaction_table.destroy()
        self.model.account_balance_db.get_balance("BTC")
        self.update_data("Binance")
        self.tc.load_transactions()
        self.load_currencies()
        self.init_bots()

    def load_currencies(self):
        self.model.base_currency = "BTC"
        self.model.target_currency = "ETH"
        self.exchange.load_data_to_model()

        self.model.target_currency_data = self.exchange.get_all_asset_names()
        self.model.update_func("base_currency_options")
        self.model.update_func("target_currency_options")

        print(self.model.asset_info.fetch_item("Binance", "BTC", "ETH"))
        print("")

    def update_data(self, exchange):#temp palcement
        dupdate = DatabaseUpdate()
        if dupdate.updated(exchange):
            print("Already updated")
            return
        d = self.exchange.prepare_binance_asset_for_db()
        for i, e in enumerate(d):
            ai = AssetInfo(exchange, e)
            self.model.asset_info.insert(ai)
            print(i)


        dupdate.set_updated(exchange="Binance", updated=True)


       # self.model.asset_info.destroy()


        #print(self.exchange.acountless_client.get_exchange_info())

    def init_bots(self):
        self.fetcher_bot = FetcherBot(self.model, self.exchange)
        self.transaction_bot = TransactionBot(self.model, self.exchange)
        self.fetcher_bot.start()
        self.transaction_bot.start()

        if self.app is not None:
            self.app.aboutToQuit.connect(self.on_exit)

    def on_exit(self):
        self.stop_bots()
        self.model.transaction_table.close()
        self.model.ta.close()

    def stop_bots(self):
        self.fetcher_bot.stop()
        self.transaction_bot.stop()

    def apply_strategy(self):
        target_procentage = self.model.strategy_target / 100.0
        stop_limit_procentage = self.model.strategy_stop_limit / 100.0

        self.model.transaction_target = self.model.transaction_buy_in * (1 + target_procentage)
        self.model.transaction_stop_limit =self.model.transaction_buy_in * (1 - stop_limit_procentage)

        d_data = self.model.asset_info.fetch_item("Binance", self.model.base_currency, self.model.target_currency)
        asset_info = AssetInfo("Binance", d_data)

        precision = asset_info.precision_price
        format_str = "{0:." + str(int(precision)) + "f}"

        self.model.transaction_target = float(format_str.format(self.model.transaction_target))
        self.model.transaction_stop_limit = float(format_str.format(self.model.transaction_stop_limit))
        self.model.update_func("transaction_target")
        self.model.update_func("transaction_stop_limit")

        print("Strategy applied")


    def execute_order(self): #change name to transaction
        item = TransactionItem(self.model.transaction_amount, self.model.transaction_buy_in, self.model.transaction_target, self.model.transaction_stop_limit, self.model.base_currency, self.model.target_currency)
        item.active = False
        item.closed = False

        item.asset_info = self.model.current_asset_info
        if self.tc.legal_transaction(item):
            print("Legal Transaction")
            self.tc.make_pending_transaction(item)
        else:
            print("Not Legal transaction")


        #print("Item added")


