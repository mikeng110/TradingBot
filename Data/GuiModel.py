

class MainModel:
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

        self.ticker_stats = []
        self.account_info = []

        self.login_msg = "" #implement later.

    def get_price(self, symbol):
        result = None

        if self.ticker_stats is None:  # exit
            return result

        for ts in self.ticker_stats:
            if ts['symbol'] == symbol:
                result = ts['price']
                break
        return result

    def get_all_asset_names(self):
        result = []

        if self.account_info is None:
            return result

        for ai in self.account_info['balances']:
            if not ai['asset'].isdigit():
                result.append(ai['asset'])
        return result

    def get_balance(self, currency):
        result = None

        if self.account_info is None:
            return result

        for ai in self.account_info['balances']:
            if ai['asset'] == currency:
                result = ai['free']
                break

        return result
