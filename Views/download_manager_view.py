from PyQt5.QtWidgets import *
from Views.gen.dowload_manager_gui import *


class DownloadManagerView(QDialog):
    def __init__(self, parent=None):
        super(DownloadManagerView, self).__init__(parent)

        self.build_ui()

    def build_ui(self):
        self.ui = Ui_Process_Gui()
        self.ui.setupUi(self)

        self.connect_signals()

    def connect_signals(self):
        pass

