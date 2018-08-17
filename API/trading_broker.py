from Model.account_model import *
from Database.Account.account import *
from API.Exchanges.binance_exchange import *
from API.Exchanges.bitmex_exchange import *
from API.Exchanges.coinbase_pro_exchange import *
import ccxt


class Exchange:

    def __init__(self, model):
        self.clients = {}
        self.connection_active = False
        self.model = model
        self.account_balance_db = None

    def fetch_price_info(self, exchange, symbol):
        self.load_exchange(exchange)
        return self.clients[exchange].fetchTicker(symbol)

    def get_currency_pairs(self, exchange):
        ret_data = {}
        self.load_exchange(exchange)

        #add logic to check if the data is already in the database and stuff.

        data = self.clients[exchange].fetchTickers()
        if data is None:
            return

        for key, value in data.items():
            temp = key.split("/")
            target = temp[0]
            base = temp[1]

            if base not in ret_data:
                ret_data[base] = ""

            ret_data[base] += target + ","

        for key, value in ret_data.items(): #remove the last comma
            ret_data[key] = value[:-1]

        return ret_data




    def get_price(self, exchange, symbol): #change to get proper price. Current hack is to use closed in case bid is none.
        if exchange in self.model.price_info:
            if symbol in self.model.price_info[exchange]:
                val = self.model.price_info[exchange][symbol]['bid']
                if val is None:
                    val = self.model.price_info[exchange][symbol]['close']
                return val

    def get_all_asset_names(self):
        return ["EOS", "ETH", "XLM", "ADA"]

    def calc_paper_balance(self, currency, amount):
        balance = self.model.paper_account_balance.balances[currency].available_balance
        balance += amount

        return balance

    def _init_paper_account_balance(self):
        self.account_balance_db = AccountBalance(self.model.db_tradingbot)
        balance = self.account_balance_db.get_all_balances()
        self.model.paper_account_balance = Balance(balance)

    def add_to_paper_balance(self, currency, amount):
        if not self.connection_active:
            self.model.paper_account_balance.balances[currency].available_balance += amount
            balance = self.model.paper_account_balance.balances[currency].available_balance

            balance_item = BalanceItem({'coin': currency, 'available_balance': balance, 'locked_balance': 0, 'btc_value': 0})
            self.model.data_writer_handler.update_balance(balance_item)

    def get_paper_balance(self, currency):
        if self.model.paper_account_balance is None:
            self._init_paper_account_balance()

        return self.model.paper_account_balance.balances[currency].available_balance

    def get_balance(self, currency):
        result = None
        if self.model.paper_trade_status:
            return self.get_paper_balance(currency)
        else:
            data = self.model.account_info

        if data is None:
            return result

        for ai in data['balances']:
            if ai['asset'] == currency:
                result = ai['free']
                break

        return result

    def get_all_asset_info(self, exchange):
        self.load_exchange(exchange)

        return self.clients[exchange].load_markets()

    def prepare_binance_asset_for_db(self): #horrible name, chnage it and chnage implementation
        data = self.get_all_asset_info("Binance")
        ret_data = []
        for key, value in data.items():
            entry_data = {}
            entry_data["base_currency"] = value["quote"]
            entry_data["target_currency"] = value['base']
            entry_data["amount_min"] = value['limits']['amount']['min']
            entry_data["amount_max"] = value['limits']['amount']['max']
            entry_data["precision_price"] = value['precision']['price']
            entry_data["precision_amount"] = value['precision']['amount']
            entry_data["precision_base_currency"] = value['precision']['quote']
            entry_data["precision_target_currency"] = value['precision']['base']

            ret_data.append(entry_data)

        return ret_data

    def load_exchange(self, exchange):
        if exchange in self.clients and self.clients[exchange] is not None:
            return

        key = "Binance"
        if exchange == key:
            self.clients[key] = BinanceExchange()
            return

        key = "Coinbase Pro"
        if exchange == key:
            self.clients[key] = CoinbaseProExchange()
            return

        key = "Bitfinex"
        if exchange == key:
            self.clients[key] = None
            return

        key = "BitMEX"
        if exchange == key:
            self.clients[key] = BitmexExchange()
            return



