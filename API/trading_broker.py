from binance.client import Client
from binance.exceptions import *
from Model.account_model import *
from Model.account_model import *
from Database.Account.account import *
import ccxt


class Exchange:

    def __init__(self, model):
        self.clients = {}
        self.client = None
        self.acountless_client = Client("","")
        self.connection_active = False
        self.model = model
        self.account_balance_db = None

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
        else:
            self.model.ticker_stats = self.acountless_client.get_all_tickers()

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

            balance_item = BalanceItem({'coin': currency, 'available_balance': balance, 'locked_balance':0, 'btc_value':0})
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
            self.clients[key] = ccxt.binance()