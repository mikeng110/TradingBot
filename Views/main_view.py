from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Views.gen.MainWindowGui import Ui_MainWindow
from Views.portfolio_manager_view import *


class MainView(QMainWindow):

    # --- Login Properties ---
    @property
    def login_api_key(self):
        return self.ui.Api_Key_tbx.text()

    @login_api_key.setter
    def login_api_key(self, value):
        pass

    @property
    def login_api_sign(self):
        return self.ui.Api_Signature_tbx.text()

    @login_api_sign.setter
    def login_api_sign(self, value):
        pass

    @property
    def login_msg(self):
        return self.ui.Login_Status_Display_lbl.text()

    @login_msg.setter
    def login_msg(self, value):
        self.ui.Login_Status_Display_lbl.setText(value)

    @property
    def logged_in(self):
        pass

    @logged_in.setter
    def logged_in(self, value):
        self.set_logged_in_mode(value)

    @property
    def paper_trade_status(self):
        return self.ui.Paper_trade_chbx.isChecked()

    @paper_trade_status.setter
    def paper_trade_status(self, value):
        pass

    # ---  Strategy Properties ----

    @property
    def strategy_target(self):
        return self.ui.Strategy_Target_Procent_hsr.value()

    @strategy_target.setter
    def strategy_target(self, value):
        self.ui.Strategy_Target_Procent_Display_lbl.setText(str(value) + "%")

    @property
    def strategy_stop_limit(self):
        return self.ui.Strategy_Stop_Limit_Procent_hsr.value()

    @strategy_stop_limit.setter
    def strategy_stop_limit(self, value):
        self.ui.Strategy_Stop_Limit_Procent_Display_lbl.setText(str(value) + "%")

    # --- Transaction Properies --
    @property
    def transaction_amount(self):
        return self.ui.Transaction_Amount_Procent_Display_hsr.value()

    @transaction_amount.setter
    def transaction_amount(self, value):
        self.ui.Transaction_Amount_Procent_Display_lbl.setText(str(value) + "%")

    @property
    def transaction_buy_in(self):
        val_str = self.ui.Transaction_Buy_in_tbx.text()
        return self.str_to_float(val_str)

    @transaction_buy_in.setter
    def transaction_buy_in(self, value):
        pass

    @property
    def transaction_target(self):
        val_str = self.ui.Transaction_Target_tbx.text()
        return self.str_to_float(val_str)

    @transaction_target.setter
    def transaction_target(self, value):
        pass

    @property
    def transaction_stop_limit(self):
        val_str = self.ui.Transaction_Stop_Limit_tbx.text()
        return self.str_to_float(val_str)

    @transaction_stop_limit.setter
    def transaction_stop_limit(self, value):
        pass

    @property
    def base_currency(self):
        return self.ui.Transaction_Currency_cbx.currentText()

    @base_currency.setter
    def base_currency(self, value):
        pass

    @property
    def target_currency(self):
        return self.ui.Transaction_Symbol_cbx.currentText()

    @target_currency.setter
    def target_currency(self, value):
        pass

    @property
    def account_balance(self):
        pass

    @account_balance.setter
    def account_balance(self, value):
        self.ui.Transaction_Account_Balance_Display_lbl.setText("Balance: " + str(value) + " " + self.model.base_currency)

    @property
    def target_price(self):
        pass

    @target_price.setter
    def target_price(self, value):
        self.ui.Transaction_Current_Price_Display_lbl.setText("Asset Price: " + str(value) + " " + self.model.base_currency)

    @property
    def base_currency_data(self):
        pass

    @base_currency_data.setter
    def base_currency_data(self, value):
        self.ui.Transaction_Currency_cbx.clear()
        self.ui.Transaction_Currency_cbx.addItems(value)

    @property
    def target_currency_data(self):
        pass

    @target_currency_data.setter
    def target_currency_data(self, value):
        self.ui.Transaction_Symbol_cbx.clear()
        self.ui.Transaction_Symbol_cbx.addItems(value)


    def __init__(self, model, main_ctrl):
        super(MainView, self).__init__()
        self.ui = None
        self.model = model
        self.main_ctrl = main_ctrl
        self.pm_ui = PortfolioManagerView()
        self.build_ui()
        self.reg_func()

    def reg_func(self):
        # register func with model for future model update announcements
        self.model.subscribe_func(self.update_login_api_key, "login_api_key")
        self.model.subscribe_func(self.update_login_api_sign, "login_api_sign")
        self.model.subscribe_func(self.update_strategy_target, "strategy_target")
        self.model.subscribe_func(self.update_strategy_stop_limit, "strategy_stop_limit")
        self.model.subscribe_func(self.update_transaction_buy_in, "transaction_buy_in")
        self.model.subscribe_func(self.update_transaction_amount, "transaction_amount")
        self.model.subscribe_func(self.update_transaction_target, "transaction_target")
        self.model.subscribe_func(self.update_transaction_stop_limit, "transaction_stop_limit")
        self.model.subscribe_func(self.update_base_currency_options, "base_currency_options")
        self.model.subscribe_func(self.update_target_currency_options, "target_currency_options")
        self.model.subscribe_func(self.update_account_balance, "account_balance")
        self.model.subscribe_func(self.update_target_price, "target_price")

    def build_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_logged_in_mode(False)
        self.init_order_views()
        self.init_strategy_view()
        self.connect_signals()

    def connect_signals(self):
        # connect signal to method
        self.ui.Api_Key_tbx.textChanged.connect(self.on_login_api_key)
        self.ui.Api_Signature_tbx.textChanged.connect(self.on_login_api_sign)
        self.ui.Login_Connect_btn.clicked.connect(self.on_login_btn)

        self.ui.Paper_trade_chbx.stateChanged.connect(self.on_paper_trade)

        self.ui.Strategy_Target_Procent_hsr.valueChanged.connect(self.on_strategy_target)
        self.ui.Strategy_Stop_Limit_Procent_hsr.valueChanged.connect(self.on_strategy_stop_limit)
        self.ui.Strategy_Apply_btn.clicked.connect(self.on_strategy_apply_btn)

        self.ui.Procent_Range_100_rbtn.toggled.connect(self.on_procent_range_100)
        self.ui.Procent_Range_50_rbtn.toggled.connect(self.on_procent_range_50)
        self.ui.Procent_Range_10_rbtn.toggled.connect(self.on_procent_range_10)

        self.ui.Transaction_Amount_Procent_Display_hsr.valueChanged.connect(self.on_transaction_amount)
        self.ui.Transaction_Buy_in_tbx.textChanged.connect(self.on_transaction_buy_in)
        self.ui.Transaction_Target_tbx.textChanged.connect(self.on_transaction_target)
        self.ui.Transaction_Stop_Limit_tbx.textChanged.connect(self.on_transaction_stop_limit)

        self.ui.Transaction_Currency_cbx.currentIndexChanged.connect(self.on_base_currency)
        self.ui.Transaction_Symbol_cbx.currentIndexChanged.connect(self.on_target_currency)
        self.ui.Transaction_Execute_btn.clicked.connect(self.on_execute_btn)

        self.ui.Menu_Transactions_Import.triggered.connect(self.on_menu_transactions_import)
        self.ui.Menu_Transactions_Export.triggered.connect(self.on_menu_transactions_export)

        self.ui.Menu_Portfolio_View.triggered.connect(self.on_portfolio_manager_view)

    def init_order_views(self):
        self.model.pending_order_model = QStandardItemModel()
        self.model.active_order_model = QStandardItemModel()
        self.model.closed_order_model = QStandardItemModel()

        self.ui.Pending_Orders_lbx.setModel(self.model.pending_order_model)
        self.ui.Filed_Orders_lbx.setModel(self.model.active_order_model)
        self.ui.Closed_Orders_lbx.setModel(self.model.closed_order_model)

    def init_strategy_view(self):
        self.ui.Procent_Range_100_rbtn.setChecked(True)

    def set_logged_in_mode(self, logged_in):
        self.ui.Strategy_gbx.setEnabled(logged_in)
        self.ui.Transaction_gbx.setEnabled(logged_in)
        self.ui.Login_gbx.setEnabled(not logged_in)


    def on_login_btn(self):
        self.main_ctrl.login()
        self.login_msg = self.model.login_msg
        self.logged_in = self.model.logged_in

    def on_login_api_key(self):
        self.main_ctrl.change_login_api_key(self.login_api_key)

    def on_login_api_sign(self):
        self.main_ctrl.change_login_api_sign(self.login_api_sign)

    def on_paper_trade(self):
        self.main_ctrl.change_paper_trade_status(self.paper_trade_status)
        self.set_logged_in_mode(self.paper_trade_status)

    def on_strategy_target(self):
        self.main_ctrl.change_strategy_target(self.strategy_target)

    def on_strategy_stop_limit(self):
        self.main_ctrl.change_strategy_stop_limit(self.strategy_stop_limit)

    def on_procent_range_100(self, enabled):
        if enabled:
            self.main_ctrl.change_strategy_sliders_weight(1)

    def on_procent_range_50(self, enabled):
        if enabled:
            self.main_ctrl.change_strategy_sliders_weight(2)

    def on_procent_range_10(self, enabled):
        if enabled:
            self.main_ctrl.change_strategy_sliders_weight(10)

    def on_strategy_apply_btn(self):
        self.main_ctrl.apply_strategy()
        self.transaction_target = self.model.transaction_target
        self.transaction_stop_limit = self.model.transaction_stop_limit

    def on_transaction_amount(self):
        self.main_ctrl.change_transaction_amount(self.transaction_amount)

    def on_transaction_buy_in(self):
        self.main_ctrl.change_transaction_buy_in(self.transaction_buy_in)

    def on_transaction_target(self):
        self.main_ctrl.change_transaction_target(self.transaction_target)

    def on_transaction_stop_limit(self):
        self.main_ctrl.change_transaction_stop_limit(self.transaction_stop_limit)

    def on_base_currency(self):
        self.main_ctrl.change_base_currency(self.base_currency)

    def on_target_currency(self):
        self.main_ctrl.change_target_currency(self.target_currency)

    def on_execute_btn(self):
        self.main_ctrl.execute_order()

    def on_menu_transactions_import(self):
        self.main_ctrl.import_transactions()

    def on_menu_transactions_export(self):
        self.main_ctrl.export_transactions()

    def on_portfolio_manager_view(self):
        self.pm_ui.exec_()

    #

    def update_login_api_key(self):
        self.login_api_key = self.model.login_api_key

    def update_login_api_sign(self):
        self.login_api_sign = self.model.login_api_sign

    def update_strategy_target(self):
        self.strategy_target = self.model.strategy_target

    def update_strategy_stop_limit(self):
        self.strategy_stop_limit = self.model.strategy_stop_limit

    def update_transaction_amount(self):
        self.transaction_amount = self.model.transaction_amount

    def update_transaction_buy_in(self):
        self.transaction_buy_in = self.model.transaction_buy_in

    def update_transaction_target(self):
        self.transaction_target = self.model.transaction_target

    def update_transaction_stop_limit(self):
        self.transaction_stop_limit = self.model.transaction_stop_limit

    def update_account_balance(self):
        self.account_balance = self.model.account_balance

    def update_target_price(self):
        self.target_price = self.model.target_price

    def update_base_currency_options(self):
        self.base_currency_data = self.model.base_currency_data

    def update_target_currency_options(self):
        self.target_currency_data = self.model.target_currency_data

    #
    #
    #

    def str_to_float(self, str): #move this to proper place.
        precision = 10
        if str == "" or str is None or str == "None":
            return round(0.0, precision)
        try:
            return round(float(str), precision)
        except ValueError:
            print("invalid format, expected decimal.")