# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboardDialog.ui'
#
# Created: Wed Feb 11 09:25:47 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dashboardDialog(object):
    def setupUi(self, dashboardDialog):
        dashboardDialog.setObjectName("dashboardDialog")
        dashboardDialog.resize(629, 675)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dashboardDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(dashboardDialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(609, 0))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setKerning(True)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.btn_AUTO = QtWidgets.QPushButton(dashboardDialog)
        self.btn_AUTO.setObjectName("btn_AUTO")
        self.verticalLayout.addWidget(self.btn_AUTO)
        self.btn_RTL = QtWidgets.QPushButton(dashboardDialog)
        self.btn_RTL.setObjectName("btn_RTL")
        self.verticalLayout.addWidget(self.btn_RTL)
        self.btn_beginFollow = QtWidgets.QPushButton(dashboardDialog)
        self.btn_beginFollow.setObjectName("btn_beginFollow")
        self.verticalLayout.addWidget(self.btn_beginFollow)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_setSubswarm = QtWidgets.QPushButton(dashboardDialog)
        self.btn_setSubswarm.setObjectName("btn_setSubswarm")
        self.horizontalLayout.addWidget(self.btn_setSubswarm)
        self.spin_setSubswarm = QtWidgets.QSpinBox(dashboardDialog)
        self.spin_setSubswarm.setMaximum(50)
        self.spin_setSubswarm.setObjectName("spin_setSubswarm")
        self.horizontalLayout.addWidget(self.spin_setSubswarm)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

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
        item.setText(_translate("dashboardDialog", "SS_ID"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("dashboardDialog", "Link"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("dashboardDialog", "Batt"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("dashboardDialog", "GPS"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("dashboardDialog", "Mode"))
        self.btn_AUTO.setText(_translate("dashboardDialog", "AUTO"))
        self.btn_RTL.setText(_translate("dashboardDialog", "RTL"))
        self.btn_beginFollow.setText(_translate("dashboardDialog", "Begin Following"))
        self.btn_setSubswarm.setText(_translate("dashboardDialog", "Assign to Subswarm"))

