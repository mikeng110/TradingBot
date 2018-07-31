# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'portfolio_manager_gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PortfolioWindow(object):
    def setupUi(self, PortfolioWindow):
        PortfolioWindow.setObjectName("PortfolioWindow")
        PortfolioWindow.resize(600, 622)
        PortfolioWindow.setStyleSheet("")
        self.Portfolio_Graph = QtWidgets.QWidget(PortfolioWindow)
        self.Portfolio_Graph.setGeometry(QtCore.QRect(40, 60, 521, 221))
        self.Portfolio_Graph.setStyleSheet("background-color: rgb(240, 240, 240)")
        self.Portfolio_Graph.setObjectName("Portfolio_Graph")
        self.label = QtWidgets.QLabel(PortfolioWindow)
        self.label.setGeometry(QtCore.QRect(40, 10, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(PortfolioWindow)
        self.label_2.setGeometry(QtCore.QRect(480, 10, 91, 16))
        self.label_2.setObjectName("label_2")
        self.tableWidget = QtWidgets.QTableWidget(PortfolioWindow)
        self.tableWidget.setGeometry(QtCore.QRect(40, 320, 521, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)

        self.retranslateUi(PortfolioWindow)
        QtCore.QMetaObject.connectSlotsByName(PortfolioWindow)

    def retranslateUi(self, PortfolioWindow):
        _translate = QtCore.QCoreApplication.translate
        PortfolioWindow.setWindowTitle(_translate("PortfolioWindow", "Dialog"))
        self.label.setText(_translate("PortfolioWindow", "Total Portfolio Value"))
        self.label_2.setText(_translate("PortfolioWindow", "Portfolio Change"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("PortfolioWindow", "Asset"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("PortfolioWindow", "Holdings"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("PortfolioWindow", "Price"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PortfolioWindow = QtWidgets.QDialog()
    ui = Ui_PortfolioWindow()
    ui.setupUi(PortfolioWindow)
    PortfolioWindow.show()
    sys.exit(app.exec_())

