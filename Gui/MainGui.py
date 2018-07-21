from PyQt5.QtWidgets import *

from MainWindowGui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, gui_data, temp_gui_data,  parent=None):
        super(MainWindow, self).__init__(parent)
        self.gui_data = gui_data
        self.temp_gui_data = temp_gui_data
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def init_gui(self):
        self.ui.Strategy_Target_Procent_hsr.sliderMoved.connect(self.slider_strategy_target)
        self.ui.Strategy_Stop_Limit_Procent_hsr.sliderMoved.connect(self.slider_strategy_stop_limit)
        self.ui.Transaction_Amount_Procent_Display_hsr.sliderMoved.connect(self.slider_transaction_amount)
        self.ui.Transaction_Amount_Procent_Display_hsr.sliderMoved.connect(self.transaction_change)
        self.ui.Transaction_Buy_in_tbx.textChanged.connect(self.transaction_change)
        self.ui.Transaction_Target_tbx.textChanged.connect(self.transaction_change)
        self.ui.Transaction_Stop_Limit_tbx.textChanged.connect(self.transaction_change)


    def set_logged_in_mode(self, logged_in):
        self.ui.Strategy_gbx.setEnabled(logged_in)
        self.ui.Transaction_gbx.setEnabled(logged_in)
        self.ui.Login_gbx.setEnabled(not logged_in)

    def setup_combo(self):
        self.ui.Transaction_Currency_cbx.addItems(["BTC", "BNB", "ETH", "USDT"])
        self.ui.Transaction_Currency_cbx.setCurrentIndex(0)

        self.ui.Transaction_Symbol_cbx.addItems(self.gui_data.get_all_asset_names())
        self.ui.Transaction_Symbol_cbx.setCurrentIndex(1)

        self.change_combo()


        self.ui.Transaction_Currency_cbx.currentIndexChanged.connect(self.change_combo)
        self.ui.Transaction_Symbol_cbx.currentIndexChanged.connect(self.change_combo)


    def change_combo(self): #bug tries to get data from invalid symbol
        self.gui_data.currency = self.ui.Transaction_Currency_cbx.currentText()
        self.gui_data.item = self.ui.Transaction_Symbol_cbx.currentText()

        current_price = self.gui_data.get_price(self.gui_data.item + self.gui_data.currency)

        if current_price is not None:
            self.ui.Transaction_Buy_in_tbx.setText(str(current_price))
            self.ui.Transaction_Status_Display_lbl.setText("Status:")
            self.ui.Transaction_Execute_btn.setEnabled(True)
        else:
            self.ui.Transaction_Status_Display_lbl.setText( "Status: Item is not on the market in " + self.gui_data.currency)
            self.ui.Transaction_Execute_btn.setEnabled(False)

    def transaction_change(self):
        self.gui_data.transaction_amount = self.str_to_float(self.ui.Transaction_Amount_Procent_Display_hsr.value())
        self.gui_data.transaction_buy_in = self.str_to_float(self.ui.Transaction_Buy_in_tbx.text())
        self.gui_data.transaction_target = self.str_to_float(self.ui.Transaction_Target_tbx.text())
        self.gui_data.transaction_stop_limit = self.str_to_float(self.ui.Transaction_Stop_Limit_tbx.text())

    def slider_strategy_target(self, value):
        self.temp_gui_data.strategy_target = value

        self.ui.Strategy_Target_Procent_Display_lbl.text = str(value) + "%"
        self.ui.Strategy_Target_Procent_Display_lbl.setText(str(value) + "%")

    def slider_strategy_stop_limit(self, value):
        self.temp_gui_data.strategy_stop_limit = value
        self.ui.Strategy_Stop_Limit_Procent_Display_lbl.setText(str(value) + "%")

    def slider_transaction_amount(self, value):
        self.temp_gui_data.transaction_amount = value
        self.ui.Transaction_Amount_Procent_Display_lbl.setText(str(value) + "%")

    def strategy_apply(self):
        self.gui_data.strategy_target = self.temp_gui_data.strategy_target
        self.gui_data.strategy_stop_limit = self.temp_gui_data.strategy_stop_limit
        self.gui_data.transaction_amount = self.temp_gui_data.transaction_amount

        transaction_buy_in = self.str_to_float(self.ui.Transaction_Buy_in_tbx.text())

        strategy_target = self.gui_data.strategy_target
        strategy_stop_limit = self.gui_data.strategy_stop_limit

        new_transaction_target = transaction_buy_in * (1 + strategy_target / 100.0)
        new_transaction_stop_limit = transaction_buy_in * (1 - strategy_stop_limit / 100.0)

        new_transaction_stop_limit = round(new_transaction_stop_limit, 10)
        new_transaction_target = round(new_transaction_target, 10)

        self.ui.Transaction_Target_tbx.setText(str(new_transaction_target))
        self.ui.Transaction_Stop_Limit_tbx.setText(str(new_transaction_stop_limit))


    def str_to_float(self, str):
        precision = 10
        if str == "":
            return round(0.0, precision)
        try:
            return round(float(str), precision)
        except ValueError:
            print ("invalid format, expected decimal.")