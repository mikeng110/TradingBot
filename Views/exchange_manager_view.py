from PyQt5.QtWidgets import *
from Views.gen.ExchangeManagerGui import *
from Controllers.exchange_manager_ctrl import *


class ExchangeManagerView(QDialog):
    def __init__(self, model, parent=None):
        super(ExchangeManagerView, self).__init__(parent)
        self.model = model
        self.ui = None

        self.emc = ExchangeManagerCtrl(model)
        self.build_ui()
        self.init_exchange_data()

    def build_ui(self):
        self.ui = Ui_Exchange_Form()
        self.ui.setupUi(self)
        self.connect_signals()

    def connect_signals(self):
        self.ui.Paper_Trade_cbx.stateChanged.connect(self.on_paper_trade)
        self.ui.Exchange_lvw.itemClicked.connect(self.on_exchange_selected)
        self.ui.download_update_btn.clicked.connect(self.on_download)

    def init_exchange_data(self):
        database_update_db = DatabaseUpdate(self.model.db_exchange)
        self.emc.downloaded_exchanges = database_update_db.get_updated()

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
        if value.text() in self.emc.downloaded_exchanges:
            self.lock_login(False)
        else:
            self.lock_login(True)

    def on_download(self):
        exchange = self.ui.Exchange_lvw.currentItem().text()
        self.emc.update_data(exchange, self.ui.progressBar)





