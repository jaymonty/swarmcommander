# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboardDialog.ui'
#
# Created: Thu Oct 30 12:31:53 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dashboardDialog(object):
    def setupUi(self, dashboardDialog):
        dashboardDialog.setObjectName("dashboardDialog")
        dashboardDialog.resize(487, 653)
        self.tableWidget = QtWidgets.QTableWidget(dashboardDialog)
        self.tableWidget.setGeometry(QtCore.QRect(40, 30, 411, 521))
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
        self.pushButton = QtWidgets.QPushButton(dashboardDialog)
        self.pushButton.setGeometry(QtCore.QRect(210, 580, 85, 27))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(dashboardDialog)
        QtCore.QMetaObject.connectSlotsByName(dashboardDialog)

    def retranslateUi(self, dashboardDialog):
        _translate = QtCore.QCoreApplication.translate
        dashboardDialog.setWindowTitle(_translate("dashboardDialog", "Dashboard"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("dashboardDialog", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("dashboardDialog", "Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("dashboardDialog", "Link"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("dashboardDialog", "Batt"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("dashboardDialog", "GPS"))
        self.pushButton.setText(_translate("dashboardDialog", "PushButton"))

