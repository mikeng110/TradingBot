# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dowload_Manager_gui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Process_Gui(object):
    def setupUi(self, Process_Gui):
        Process_Gui.setObjectName("Process_Gui")
        Process_Gui.resize(573, 532)
        self.listView = QtWidgets.QListView(Process_Gui)
        self.listView.setGeometry(QtCore.QRect(40, 30, 491, 441))
        self.listView.setObjectName("listView")
        self.progressBar = QtWidgets.QProgressBar(Process_Gui)
        self.progressBar.setGeometry(QtCore.QRect(40, 490, 521, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(Process_Gui)
        QtCore.QMetaObject.connectSlotsByName(Process_Gui)

    def retranslateUi(self, Process_Gui):
        _translate = QtCore.QCoreApplication.translate
        Process_Gui.setWindowTitle(_translate("Process_Gui", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Process_Gui = QtWidgets.QWidget()
    ui = Ui_Process_Gui()
    ui.setupUi(Process_Gui)
    Process_Gui.show()
    sys.exit(app.exec_())

