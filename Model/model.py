from Database.Exchange.tradeable_assets import *
from Database.Account.account import *

from Model.database_handler import *
from Utils_Library.utils import *
import queue


class Model(object):
    def __init__(self):

        self.utils = Utils()

        self.req_queue = None
        self.data_writer_handler = None

        self._update_funcs = []
        self._update_func_seperate = {}
        self.graphics_mode = True

        self.active_order_model = None
        self.pending_order_model = None
        self.closed_order_model = None

        self.paper_trade_status = False

        # --- Databases ----
        self.db_tradingbot = None
        self.db_exchange = None

        # --- Data ----
        self.current_asset_info = None
        self.base_currency_data = ["BTC", "BNB", "ETH", "USDT"]
        self.target_currency_data = []
        self.currency_data = {}

        self.price_info = {}
        self.account_info = []
        self.transactions = []

        self.base_currency = ""
        self.target_currency = ""

        self.account_balance = 0
        self.paper_account_balance = None
        self.target_price = 0

        # --- Login Properties ---
        self.login_api_key = ""
        self.login_api_sign = ""
        self.logged_in = False
        self.login_msg = ""

        # ---  Strategy Properties ----
        self.strategy_target = 0
        self.strategy_stop_limit = 0
        self.strategy_slider_weight = 1

        # --- Transaction Properties ---
        self.transaction_amount = 0
        self.transaction_buy_in = 0
        self.transaction_target = 0
        self.transaction_stop_limit = 0

#

    def close_transaction(self, transaction):
        transaction.closed = True

    def init_data(self): #move to controller
        self.db_tradingbot = Database("TradingBot.db")
        self.db_exchange = Database("Database/Exchange.db")

        self.req_queue = queue.Queue()
        self.data_writer_handler = DatabaseHandlerModel(self.req_queue)

       # data = self.exchange.get_currency_pairs("Binance")

        #tradable_asset.load(data, "Binance")
        tradable_asset = TradableAsset(self.db_exchange)
        self.currency_data = tradable_asset.fetch("Binance")

    def save_transactions(self):
        print("Update database")
        for transaction in self.transactions:
            pass


    # subscribe a view method for updating
    def subscribe_func(self, func, key = None):
       # print("Subscribe")
        if key is not None:
            self._update_func_seperate[key] = func


    # unsubscribe a view method for updating
    def unsubscribe_update_func(self, func):
      #  print("Unsubscribe")
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    # update registered view methods
    def announce_update(self):
        for func in self._update_funcs:
            func()

    def update_func(self, key):
        if key in self._update_func_seperate:
            self._update_func_seperate[key]()