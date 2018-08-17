import ccxt

class CoinbaseProExchange:
    def __init__(self):
        self.connection = None
        self.init()


    def init(self):
        self.connection = ccxt.coinbasepro({
                'enableRateLimit': True,
            })

    def fetchTicker(self, symbol):
        return self.connection.fetchTicker(symbol)

    def load_markets(self): #refactor so data format is from 1 place
        ret_data = {}
        data = self.connection.load_markets()
        for key, value in data.items():
            if value["active"] == False:
                continue

            temp = {}
            temp["symbol"] = value["symbol"]
            temp["base_currency"] = value["quote"]
            temp["target_currency"] = value["base"]
            temp["amount_min"] = value["limits"]["amount"]["min"]
            temp["amount_max"] = value["limits"]["amount"]["max"]
            temp["precision_price"] = value["precision"]["price"]
            temp["precision_amount"] = value["precision"]["amount"]
            temp["precision_base_currency"] = 8
            temp["precision_target_currency"] = 8

            ret_data[key] = temp
        return ret_data