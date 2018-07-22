from binance.client import Client
from binance.exceptions import *

class Bot:
    def __init__(self, api_key, api_signature):
        self.connected = False
        self.client = None
        self.connect(api_key, api_signature)

    def connect(self, api_key, api_signature):
        if self.connected:
            return None

        try:
            self.client = Client(api_key, api_signature)

            self.client.get_account()
            self.connected = True

        except BinanceAPIException as e:
            print("Wrong Api Key, or wrong Api Signature")
            self.connected = False

    def get_all_tickers(self):
        return self.client.get_all_tickers()

    def get_account_info(self):
        return self.client.get_account()

