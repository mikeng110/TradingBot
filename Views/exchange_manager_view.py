from PyQt5.QtWidgets import *

from Views.gen.ExchangeManagerGui import *


class ExchangeManagerView(QDialog): #maybe make it a widget or something else. multiple main windows create problems

    def __init__(self, parent=None):
        super(ExchangeManagerView, self).__init__(parent)
        self.ui = None

        self.build_ui()

    def build_ui(self):
        self.ui = Ui_Exchange_Form()
        self.ui.setupUi(self)
        self.connect_signals()

    def connect_signals(self):
        self.ui.Paper_Trade_cbx.stateChanged.connect(self.on_paper_trade)
        self.ui.Login_Connect_btn.clicked.connect(self.buildExamplePopup)


    def on_paper_trade(self, value):
        self.ui.Api_Key_tbx.setEnabled(not value)
        self.ui.Api_Signature_tbx.setEnabled(not value)

    def buildExamplePopup(self):
        exPopup = ExamplePopup(self)
        exPopup.setGeometry(100, 200, 100, 100)
        exPopup.show()



class ExamplePopup(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
