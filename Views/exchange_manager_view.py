from PyQt5.QtWidgets import *
from Database.database_update import *
from Views.gen.ExchangeManagerGui import *
from Database.Exchange.asset_info import *
from API.trading_broker import *
from Model.asset_info import *
from PyQt5.QtCore import *
from Database.Exchange.tradeable_assets import *

from Views.download_manager_view import *


class ExchangeManagerView(QDialog):

    def __init__(self, model, parent=None):
        super(ExchangeManagerView, self).__init__(parent)
        self.model = model

        self.dm_ui = None
        self.timer = QBasicTimer()
        self.step = 0

        self.ui = None
        self.build_ui()
        self.downloaded_exchanges = []

        self.init_exchange_data()



    def build_ui(self):
        self.ui = Ui_Exchange_Form()
        self.ui.setupUi(self)
        self.dm_ui = DownloadManagerView()
        self.connect_signals()


    def connect_signals(self):
        self.ui.Paper_Trade_cbx.stateChanged.connect(self.on_paper_trade)
        self.ui.Exchange_lvw.itemClicked.connect(self.on_exchange_selected)
        self.ui.download_update_btn.clicked.connect(self.on_download)

    def init_exchange_data(self):
        database_update_db = DatabaseUpdate(self.model.db_exchange)
        self.downloaded_exchanges = database_update_db.get_updated()

        data = ["Binance", "Coinbase Pro", "BitMEX"]
        for exchange in data:

            item = QListWidgetItem(exchange)
            self.ui.Exchange_lvw.addItem(item)

        self.ui.Exchange_lvw.setCurrentRow(0)
        self.on_exchange_selected(self.ui.Exchange_lvw.currentItem())

    def lock_login(self, value):
        self.ui.Login_gbx.setEnabled(not value)

    def on_paper_trade(self, value):
        self.ui.Api_Key_tbx.setEnabled(not value)
        self.ui.Api_Signature_tbx.setEnabled(not value)

    def on_exchange_selected(self, value):
        if value.text() in self.downloaded_exchanges:
            self.lock_login(False)
        else:
            self.lock_login(True)

    def on_download(self):
        exchange = self.ui.Exchange_lvw.currentItem().text()
        self.update_data(exchange)


    def update_data(self, exchange):

        database_update_db = DatabaseUpdate(self.model.db_exchange)
        asset_info_db = AssetInfoDB(self.model.db_exchange)
        asset_info_db.clear(exchange)

        trading_broker = Exchange(self.model)
        data = trading_broker.get_all_asset_info(exchange)

        assets = TradableAsset(self.model.db_exchange)


        length = len(data)
        print(length)

        currency_pairs = trading_broker.get_currency_pairs(exchange, data)
        prepared_data = trading_broker.parse_asset_info(exchange, data)
        assets.load(currency_pairs, exchange)
        self.step = 0
        for i, e in enumerate(prepared_data):
            ai = AssetInfo(exchange, e)
            asset_info_db.insert(ai)
            print(i)
            self.step += 100.0/length
            self.ui.progressBar.setValue(self.step)

        database_update_db.set_updated(exchange=exchange, updated=True)
        self.downloaded_exchanges = database_update_db.get_updated()
        self.ui.progressBar.setValue(100)


