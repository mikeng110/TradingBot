import ccxt
from Utils_Library.utils import *
class BinanceExchange:
    def __init__(self):
        self.connection = None
        self.utils = None
        self.init()


    def init(self):
        self.utils = Utils()
        self.connection = ccxt.binance({
                'enableRateLimit': True,
            })

    def fetchTicker(self, symbol):
        return self.connection.fetchTicker(symbol)

    def load_markets(self):
        ret_data = {}
        data = self.connection.load_markets()
        for key, value in data.items():
            if value["active"] == False:
                continue

            ret_data[key] = self.utils.parse_market_entry(value)
        return ret_data