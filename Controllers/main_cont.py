from API.trading_broker import *
from Bot.fetcher_bot import *
from Bot.transaction_bot import *
from Controllers.transaction_ctrl import *
from Model.io_transactions import *
from Model.asset_info import *
from Database.database_update import *
from Model.database_handler import *
from Model.account_model import *
from Bot.database_writer import *
import time

from Database.Exchange.asset_info import *
from Database.Exchange.tradeable_assets import *



class MainController(object):

    def __init__(self, model, app=None):
        self.model = model
        self.exchange = Exchange(model)
        self.fetcher_bot = None
        self.transaction_bot = None
        self.db_writer_bot = None
        self.app = app
        self.asset_info_db = None
        self.account_balance_db = None

        self.temp_exchange_holder = "" #change name

        self.model.init_data()

        if self.app is not None:
            self.model.graphics_mode = True
        else:
            self.model.graphics_mode = False
        self.tc = TransactionCtrl(model, self.exchange)

    def change_exchange(self, value):
        self.model.current_exchange = value

    def change_login_api_key(self, value):
        self.model.login_api_key = value
        self.model.update_func("login_api_key")

    def change_login_api_sign(self, value):
        self.model.login_api_sign = value
        self.model.update_func("login_api_sign")

    def change_strategy_target(self, value):

        self.model.strategy_target = value / self.model.strategy_slider_weight
        self.model.update_func("strategy_target")

    def change_strategy_stop_limit(self, value):
        self.model.strategy_stop_limit = value / self.model.strategy_slider_weight
        self.model.update_func("strategy_stop_limit")

    def change_strategy_sliders_weight(self, value):
        self.model.strategy_slider_weight = value

    def change_paper_trade_status(self, value):
        self.model.paper_trade_status = value
        if value:
            self.paper_login()

    def change_transaction_amount(self, value):
        self.model.transaction_amount = value
        self.model.update_func("transaction_amount")

    def change_transaction_buy_in(self, value):
        self.model.transaction_buy_in = value
        self.model.update_func("transaction_buy_in")

    def change_transaction_target(self, value):
        self.model.transaction_target = value
        self.model.update_func("transaction_target")

    def change_transaction_stop_limit(self, value):
        self.model.transaction_stop_limit = value
        self.model.update_func("transaction_stop_limit")

    def change_base_currency(self, value):
        self.model.base_currency = value
        self.model.target_currency_data = self.model.currency_data[value]
        self.model.target_currency = self.model.target_currency_data[0]

        if self.model.base_currency != '' and self.model.target_currency != '':  # rewrite so this is not needed
            d_data = self.asset_info_db.fetch_item(self.model.current_exchange, self.model.base_currency, self.model.target_currency)
            self.model.current_asset_info = AssetInfo(self.model.current_exchange, d_data)

        self.model.update_func("target_currency_options")

    def change_target_currency(self, value):
        self.model.target_currency = value

        if self.model.base_currency != '' and self.model.target_currency != '': #rewrite so this is not needed
            d_data = self.asset_info_db.fetch_item(self.model.current_exchange, self.model.base_currency, self.model.target_currency)
            self.model.current_asset_info = AssetInfo(self.model.current_exchange, d_data)

    def change_account_balance(self, value):
        self.model.account_balance = value
        self.model.update_func("account_balance")

    def import_transactions(self):
        io = IoTransactions(self.model.transactions)
        t_list = io.import_file("Exported.txt")

    def export_transactions(self):
        io = IoTransactions(self.model.transactions)
        io.export_file("Exported.txt")

    def paper_login(self):
       # self.model.base_currency = "BTC"
       # self.model.target_currency = "ETH"
        self.model.paper_trade_status = True
        self.load_exchange_data()
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

    def load_paper_balance(self):
        balance_item = BalanceItem({'coin': 'BTC', 'available_balance': 50, 'locked_balance':0, 'btc_value':0})
        self.model.data_writer_handler.update_balance(balance_item)
        balance_item = BalanceItem({'coin': 'BNB', 'available_balance': 80, 'locked_balance': 0, 'btc_value': 0})
        self.model.data_writer_handler.update_balance(balance_item)
        balance_item = BalanceItem({'coin': 'ETH', 'available_balance': 120, 'locked_balance': 0, 'btc_value': 0})
        self.model.data_writer_handler.update_balance(balance_item)
        balance_item = BalanceItem({'coin': 'USDT', 'available_balance': 200, 'locked_balance': 0, 'btc_value': 0})
        self.model.data_writer_handler.update_balance(balance_item)

    def login_procedure(self):
        self.model.logged_in = True
        self.asset_info_db = AssetInfoDB(self.model.db_exchange)
       # self.update_data("Binance")
        self.tc.load_transactions()
        self.load_currencies()

        self.init_bots()

    def load_exchange_data(self):
        database_update_db = DatabaseUpdate(self.model.db_exchange)
        self.model.exchanges_data = database_update_db.get_updated()

        if len(self.model.exchanges_data) > 0:
            if self.model.current_exchange is None:
                self.model.current_exchange = self.model.exchanges_data[0]

            self.model.update_func("exchanges_data")

    def load_currencies(self):
      #  self.model.base_currency = "BTC"
    #    self.model.target_currency = "ETH"
        #self.exchange.load_data_to_model("Binance")
        tradable_asset = TradableAsset(self.model.db_exchange)
        self.model.currency_data = tradable_asset.fetch(self.model.current_exchange)

        self.model.base_currency_data = self.get_base_currency_data(self.model.currency_data)  #self.exchange.get_all_asset_names()
        first = next(iter(self.model.currency_data))
        self.model.target_currency_data = self.model.currency_data[first]
        self.model.update_func("base_currency_options")
        self.model.update_func("target_currency_options")

    def update_data(self, exchange):
        database_update_db = DatabaseUpdate(self.model.db_exchange)
        print(database_update_db.get_updated())

        if database_update_db.updated("Binance"):
            print("Already updated")
            return

        self.asset_info_db.clear("Binance")

        d = self.exchange.prepare_binance_asset_for_db()
        for i, e in enumerate(d):
            ai = AssetInfo("Binance", e)
            self.asset_info_db.insert(ai)
            print(i)

        database_update_db.set_updated(exchange="Binance", updated=True)

    def init_bots(self):
        self.fetcher_bot = FetcherBot(self.model, self.exchange)
        self.transaction_bot = TransactionBot(self.model, self.exchange)
        self.db_writer_bot = DataWriterBot(self.model)

        self.fetcher_bot.start()
        self.transaction_bot.start()
        self.db_writer_bot.start()

        if self.app is not None:
            self.app.aboutToQuit.connect(self.on_exit)

    def on_exit(self):
        self.stop_bots()

    def stop_bots(self):
        self.fetcher_bot.stop()
        self.transaction_bot.stop()
        self.db_writer_bot.stop()

    def apply_strategy(self):
        target_procentage = self.model.strategy_target / 100.0
        stop_limit_procentage = self.model.strategy_stop_limit / 100.0

        self.model.transaction_target = self.model.transaction_buy_in * (1 + target_procentage)
        self.model.transaction_stop_limit =self.model.transaction_buy_in * (1 - stop_limit_procentage)

        d_data = self.asset_info_db.fetch_item("Binance", self.model.base_currency, self.model.target_currency)
        asset_info = AssetInfo("Binance", d_data)

        precision = asset_info.precision_price
        format_str = "{0:." + str(int(precision)) + "f}"

        self.model.transaction_target = float(format_str.format(self.model.transaction_target))
        self.model.transaction_stop_limit = float(format_str.format(self.model.transaction_stop_limit))
        self.model.update_func("transaction_target")
        self.model.update_func("transaction_stop_limit")

        print("Strategy applied")

    def execute_transaction(self):
        item = TransactionItem(self.model.transaction_amount, self.model.transaction_buy_in, self.model.transaction_target, self.model.transaction_stop_limit, self.model.base_currency, self.model.target_currency)
        item.active = False
        item.closed = False

        item.asset_info = self.model.current_asset_info

        if self.tc.legal_transaction(item):
            print("Legal Transaction")
            self.tc.make_pending_transaction(item)
        else:
            print("Not Legal transaction")


    def get_base_currency_data(self, data):
        ret_data = []
        for key, value in data.items():
            ret_data.append(key)

        return ret_data





