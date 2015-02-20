# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboardDialog.ui'
#
# Created: Thu Feb 19 20:51:35 2015
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
        self.tableWidget.setColumnCount(8)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.btn_AUTO = QtWidgets.QPushButton(dashboardDialog)
        self.btn_AUTO.setObjectName("btn_AUTO")
        self.verticalLayout.addWidget(self.btn_AUTO)
        self.btn_RTL = QtWidgets.QPushButton(dashboardDialog)
        self.btn_RTL.setObjectName("btn_RTL")
        self.verticalLayout.addWidget(self.btn_RTL)
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.spin_selectSubswarm = QtWidgets.QSpinBox(dashboardDialog)
        self.spin_selectSubswarm.setMinimum(1)
        self.spin_selectSubswarm.setMaximum(50)
        self.spin_selectSubswarm.setObjectName("spin_selectSubswarm")
        self.gridLayout.addWidget(self.spin_selectSubswarm, 0, 1, 1, 1)
        self.lbl_selectSubswarm = QtWidgets.QLabel(dashboardDialog)
        self.lbl_selectSubswarm.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_selectSubswarm.setObjectName("lbl_selectSubswarm")
        self.gridLayout.addWidget(self.lbl_selectSubswarm, 0, 0, 1, 1)
        self.btn_suspendSwarmBehavior = QtWidgets.QPushButton(dashboardDialog)
        self.btn_suspendSwarmBehavior.setObjectName("btn_suspendSwarmBehavior")
        self.gridLayout.addWidget(self.btn_suspendSwarmBehavior, 4, 1, 1, 1)
        self.btn_beginSwarmBehavior = QtWidgets.QPushButton(dashboardDialog)
        self.btn_beginSwarmBehavior.setObjectName("btn_beginSwarmBehavior")
        self.gridLayout.addWidget(self.btn_beginSwarmBehavior, 4, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_egressSubswarm = QtWidgets.QPushButton(dashboardDialog)
        self.btn_egressSubswarm.setObjectName("btn_egressSubswarm")
        self.horizontalLayout_2.addWidget(self.btn_egressSubswarm)
        self.spin_egressSubswarm = QtWidgets.QSpinBox(dashboardDialog)
        self.spin_egressSubswarm.setMaximum(52)
        self.spin_egressSubswarm.setObjectName("spin_egressSubswarm")
        self.horizontalLayout_2.addWidget(self.spin_egressSubswarm)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

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
        item.setText(_translate("dashboardDialog", "Swarm State"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("dashboardDialog", "Link"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("dashboardDialog", "Batt"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("dashboardDialog", "GPS"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("dashboardDialog", "Mode"))
        self.btn_AUTO.setText(_translate("dashboardDialog", "AUTO"))
        self.btn_RTL.setText(_translate("dashboardDialog", "RTL Selected UAVs"))
        self.btn_setSubswarm.setText(_translate("dashboardDialog", "Assign Select UAVs to Subswarm"))
        self.lbl_selectSubswarm.setText(_translate("dashboardDialog", "Select Subswarm for Behavior Command:  "))
        self.btn_suspendSwarmBehavior.setText(_translate("dashboardDialog", "Suspend Swarm Behavior"))
        self.btn_beginSwarmBehavior.setText(_translate("dashboardDialog", "Begin Swarm Behavior"))
        self.btn_egressSubswarm.setText(_translate("dashboardDialog", "Subswarm Egress"))

