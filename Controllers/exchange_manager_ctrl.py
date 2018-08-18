from Database.database_update import *
from Database.Exchange.tradeable_assets import *
from Database.Exchange.asset_info import *
from API.trading_broker import *
from Model.asset_info import *

class ExchangeManagerCtrl:
    def __init__(self, model):
        self.model = model
        self.database_update_db = None
        self.asset_info_db = None
        self.trading_broker = None
        self.assets = None
        self.downloaded_exchanges = []

        self.init()

    def init(self):
        self.database_update_db = DatabaseUpdate(self.model.db_exchange)
        self.asset_info_db = AssetInfoDB(self.model.db_exchange)
        self.trading_broker = Exchange(self.model)
        self.assets = TradableAsset(self.model.db_exchange)

    def update_data(self, exchange, progress_bar):
        self.asset_info_db.clear(exchange)
        data = self.trading_broker.get_all_asset_info(exchange)

        length = len(data)

        currency_pairs = self.trading_broker.get_currency_pairs(exchange, data)
        prepared_data = self.trading_broker.parse_asset_info(exchange, data)

        self.assets.load(currency_pairs, exchange)

        step = 0
        for i, e in enumerate(prepared_data):
            ai = AssetInfo(exchange, e)
            self.asset_info_db.insert(ai)
            print(i)
            step += 100.0/length
            progress_bar.setValue(step)

        self.database_update_db.set_updated(exchange=exchange, updated=True)
        self.downloaded_exchanges = self.database_update_db.get_updated()
        progress_bar.setValue(100)

