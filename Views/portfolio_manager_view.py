from PyQt5.QtWidgets import *


from Controllers.portfolio_manager_ctrl import *

from Views.gen.portfolio_manager_gui import Ui_PortfolioWindow


class PortfolioManagerView(QDialog): #maybe make it a widget or something else. multiple main windows create problems

    @property
    def portfolio_graph(self):
        pass

    @portfolio_graph.setter
    def portfolio_graph(self, value):
        layout = QVBoxLayout()
        layout.addWidget(value)
        self.ui.Portfolio_Graph.setLayout(layout)

    def __init__(self, parent=None):
        super(PortfolioManagerView, self).__init__(parent)
        self.ui = None
        self.pmc = PortfolioManagerCtrl()

        self.build_ui()

    def build_ui(self):
        self.ui = Ui_PortfolioWindow()
        self.ui.setupUi(self)
        self.setup_portfolio_graph()
        self.connect_signals()

    def connect_signals(self):
        pass

    def setup_portfolio_graph(self):
        self.portfolio_graph = self.pmc.get_canvas()
        self.pmc.plot()