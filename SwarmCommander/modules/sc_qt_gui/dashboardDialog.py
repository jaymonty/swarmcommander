# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboardDialog.ui'
#
# Created: Mon Oct 27 08:58:54 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dashboardDialog(object):
    def setupUi(self, dashboardDialog):
        dashboardDialog.setObjectName("dashboardDialog")
        dashboardDialog.resize(487, 653)
        self.buttonBox = QtWidgets.QDialogButtonBox(dashboardDialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 580, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableWidget = QtWidgets.QTableWidget(dashboardDialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 30, 411, 521))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        self.retranslateUi(dashboardDialog)
        self.buttonBox.accepted.connect(dashboardDialog.accept)
        self.buttonBox.rejected.connect(dashboardDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dashboardDialog)

    def retranslateUi(self, dashboardDialog):
        _translate = QtCore.QCoreApplication.translate
        dashboardDialog.setWindowTitle(_translate("dashboardDialog", "Dashboard"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("dashboardDialog", "UAV"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("dashboardDialog", "Link"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("dashboardDialog", "Batt"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("dashboardDialog", "GPS"))

