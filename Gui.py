from PyQt5.QtWidgets import *

from MainWindowGui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def set_logged_in_mode(self, logged_in):
        self.ui.Strategy_gbx.setEnabled(logged_in)
        self.ui.Transaction_gbx.setEnabled(logged_in)
        self.ui.Login_gbx.setEnabled(not logged_in)
