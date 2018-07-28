from binance.client import Client
from binance.exceptions import *


class Exchange:

    def __init__(self, model):
        self.client = None
        self.connection_active = False
        self.model = model

    def connect(self, api_key, api_signature):
        if self.connection_active:
            return None

        self.client = Client(api_key, api_signature)

        try:
            self.client.get_account()
            self.connection_active = True

        except BinanceAPIException as e:
            print("Wrong Api Key, or wrong Api Signature")
            self.connection_active = False

    def load_data_to_model(self):
        if self.connection_active:
            self.model.account_info = self.client.get_account()
            self.model.ticker_stats = self.client.get_all_tickers()

    def get_price(self, symbol):  # remove later
        result = None

        if self.model.ticker_stats is None:  # exit
            return result

        for ts in self.model.ticker_stats:
            if ts['symbol'] == symbol:
                result = ts['price']
                break
        return result

    def get_all_asset_names(self):
        return ["EOS", "ETH", "XLM", "ADA"]
      #  result = []

       # if self.model.account_info is None:
       #     return result

       # for ai in self.model.account_info['balances']:
        #    if not ai['asset'].isdigit():
        #        result.append(ai['asset'])
       # return result

    def get_balance(self, currency):
        result = None

        if self.model.account_info is None:
            return result

        for ai in self.model.account_info['balances']:
            if ai['asset'] == currency:
                result = ai['free']
                break

        return result
