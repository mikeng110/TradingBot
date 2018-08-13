# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exchange_manager_gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Exchange_Form(object):
    def setupUi(self, Exchange_Form):
        Exchange_Form.setObjectName("Exchange_Form")
        Exchange_Form.resize(519, 512)
        self.Login_gbx = QtWidgets.QGroupBox(Exchange_Form)
        self.Login_gbx.setGeometry(QtCore.QRect(20, 340, 471, 141))
        self.Login_gbx.setObjectName("Login_gbx")
        self.Api_Key_tbx = QtWidgets.QLineEdit(self.Login_gbx)
        self.Api_Key_tbx.setGeometry(QtCore.QRect(90, 30, 351, 20))
        self.Api_Key_tbx.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Api_Key_tbx.setObjectName("Api_Key_tbx")
        self.Api_Signature_tbx = QtWidgets.QLineEdit(self.Login_gbx)
        self.Api_Signature_tbx.setGeometry(QtCore.QRect(90, 70, 351, 20))
        self.Api_Signature_tbx.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Api_Signature_tbx.setObjectName("Api_Signature_tbx")
        self.Login_Status_Display_lbl = QtWidgets.QLabel(self.Login_gbx)
        self.Login_Status_Display_lbl.setGeometry(QtCore.QRect(10, 120, 141, 16))
        self.Login_Status_Display_lbl.setObjectName("Login_Status_Display_lbl")
        self.Login_Connect_btn = QtWidgets.QPushButton(self.Login_gbx)
        self.Login_Connect_btn.setGeometry(QtCore.QRect(380, 110, 75, 23))
        self.Login_Connect_btn.setObjectName("Login_Connect_btn")
        self.label_2 = QtWidgets.QLabel(self.Login_gbx)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.Login_gbx)
        self.label.setGeometry(QtCore.QRect(10, 30, 51, 16))
        self.label.setObjectName("label")
        self.Paper_Trade_cbx = QtWidgets.QCheckBox(self.Login_gbx)
        self.Paper_Trade_cbx.setGeometry(QtCore.QRect(290, 110, 91, 21))
        self.Paper_Trade_cbx.setObjectName("Paper_Trade_cbx")
        self.Exchange_lvw = QtWidgets.QListWidget(Exchange_Form)
        self.Exchange_lvw.setGeometry(QtCore.QRect(20, 10, 471, 321))
        self.Exchange_lvw.setObjectName("Exchange_lvw")
        item = QtWidgets.QListWidgetItem()
        self.Exchange_lvw.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.Exchange_lvw.addItem(item)

        self.retranslateUi(Exchange_Form)
        QtCore.QMetaObject.connectSlotsByName(Exchange_Form)

    def retranslateUi(self, Exchange_Form):
        _translate = QtCore.QCoreApplication.translate
        Exchange_Form.setWindowTitle(_translate("Exchange_Form", "Exchange Manager"))
        self.Login_gbx.setTitle(_translate("Exchange_Form", "Login"))
        self.Login_Status_Display_lbl.setText(_translate("Exchange_Form", "Status:"))
        self.Login_Connect_btn.setText(_translate("Exchange_Form", "Connect"))
        self.label_2.setText(_translate("Exchange_Form", "Api_Signature:"))
        self.label.setText(_translate("Exchange_Form", "Api_Key:"))
        self.Paper_Trade_cbx.setText(_translate("Exchange_Form", "Paper Login"))
        __sortingEnabled = self.Exchange_lvw.isSortingEnabled()
        self.Exchange_lvw.setSortingEnabled(False)
        item = self.Exchange_lvw.item(0)
        item.setText(_translate("Exchange_Form", "Binance"))
        item = self.Exchange_lvw.item(1)
        item.setText(_translate("Exchange_Form", "Coinbase"))
        self.Exchange_lvw.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Exchange_Form = QtWidgets.QWidget()
    ui = Ui_Exchange_Form()
    ui.setupUi(Exchange_Form)
    Exchange_Form.show()
    sys.exit(app.exec_())

