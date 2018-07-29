
class Model(object):
    def __init__(self):
        self._update_funcs = []
        self._update_func_seperate = {}

        self.active_order_model = None
        self.pending_order_model = None


        # --- Data ----
        self.base_currency_data = ["BTC", "BNB", "ETH", "USDT"]
        self.target_currency_data = []
        self.ticker_stats = []
        self.account_info = []
        self.transactions = []

        self.base_currency = ""
        self.target_currency = ""

        self.account_balance = 0
        self.target_price = 0

        # --- Login Properties ---
        self.login_api_key = ""
        self.login_api_sign = ""
        self.logged_in = False
        self.login_msg = ""

        # ---  Strategy Properties ----
        self.strategy_target = 0
        self.strategy_stop_limit = 0

        # --- Transaction Properties ---
        self.transaction_amount = 0
        self.transaction_buy_in = 0
        self.transaction_target = 0
        self.transaction_stop_limit = 0



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