# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboardDialog.ui'
#
# Created: Mon Mar 23 13:24:08 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dashboardDialog(object):
    def setupUi(self, dashboardDialog):
        dashboardDialog.setObjectName("dashboardDialog")
        dashboardDialog.resize(755, 675)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dashboardDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(dashboardDialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(735, 0))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_setSubswarm = QtWidgets.QPushButton(dashboardDialog)
        self.btn_setSubswarm.setObjectName("btn_setSubswarm")
        self.gridLayout.addWidget(self.btn_setSubswarm, 2, 0, 1, 1)
        self.spin_selectSubswarm = QtWidgets.QSpinBox(dashboardDialog)
        self.spin_selectSubswarm.setMinimum(1)
        self.spin_selectSubswarm.setMaximum(50)
        self.spin_selectSubswarm.setObjectName("spin_selectSubswarm")
        self.gridLayout.addWidget(self.spin_selectSubswarm, 3, 1, 1, 1)
        self.lbl_selectSubswarm = QtWidgets.QLabel(dashboardDialog)
        self.lbl_selectSubswarm.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_selectSubswarm.setObjectName("lbl_selectSubswarm")
        self.gridLayout.addWidget(self.lbl_selectSubswarm, 3, 0, 1, 1)
        self.btn_suspendSwarmBehavior = QtWidgets.QPushButton(dashboardDialog)
        self.btn_suspendSwarmBehavior.setObjectName("btn_suspendSwarmBehavior")
        self.gridLayout.addWidget(self.btn_suspendSwarmBehavior, 7, 1, 1, 1)
        self.btn_beginSwarmBehavior = QtWidgets.QPushButton(dashboardDialog)
        self.btn_beginSwarmBehavior.setObjectName("btn_beginSwarmBehavior")
        self.gridLayout.addWidget(self.btn_beginSwarmBehavior, 7, 0, 1, 1)
        self.swarm_label = QtWidgets.QLabel(dashboardDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.swarm_label.setFont(font)
        self.swarm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.swarm_label.setObjectName("swarm_label")
        self.gridLayout.addWidget(self.swarm_label, 0, 0, 1, 2)
        self.spin_egressSubswarm = QtWidgets.QSpinBox(dashboardDialog)
        self.spin_egressSubswarm.setMaximum(52)
        self.spin_egressSubswarm.setObjectName("spin_egressSubswarm")
        self.gridLayout.addWidget(self.spin_egressSubswarm, 8, 1, 1, 1)
        self.btn_egressSubswarm = QtWidgets.QPushButton(dashboardDialog)
        self.btn_egressSubswarm.setObjectName("btn_egressSubswarm")
        self.gridLayout.addWidget(self.btn_egressSubswarm, 8, 0, 1, 1)
        self.spin_setSubswarm = QtWidgets.QSpinBox(dashboardDialog)
        self.spin_setSubswarm.setMaximum(50)
        self.spin_setSubswarm.setObjectName("spin_setSubswarm")
        self.gridLayout.addWidget(self.spin_setSubswarm, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_setSwarmState = QtWidgets.QPushButton(dashboardDialog)
        self.btn_setSwarmState.setObjectName("btn_setSwarmState")
        self.gridLayout_2.addWidget(self.btn_setSwarmState, 2, 0, 1, 1)
        self.combo_swarmState = QtWidgets.QComboBox(dashboardDialog)
        self.combo_swarmState.setObjectName("combo_swarmState")
        self.combo_swarmState.addItem("")
        self.combo_swarmState.addItem("")
        self.combo_swarmState.addItem("")
        self.combo_swarmState.addItem("")
        self.combo_swarmState.addItem("")
        self.combo_swarmState.addItem("")
        self.gridLayout_2.addWidget(self.combo_swarmState, 2, 1, 1, 1)
        self.label_overrides = QtWidgets.QLabel(dashboardDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_overrides.setFont(font)
        self.label_overrides.setAlignment(QtCore.Qt.AlignCenter)
        self.label_overrides.setObjectName("label_overrides")
        self.gridLayout_2.addWidget(self.label_overrides, 0, 0, 1, 2)
        self.btn_AUTO = QtWidgets.QPushButton(dashboardDialog)
        self.btn_AUTO.setObjectName("btn_AUTO")
        self.gridLayout_2.addWidget(self.btn_AUTO, 1, 0, 1, 1)
        self.btn_RTL = QtWidgets.QPushButton(dashboardDialog)
        self.btn_RTL.setObjectName("btn_RTL")
        self.gridLayout_2.addWidget(self.btn_RTL, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)

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
        item.setText(_translate("dashboardDialog", "Ctrl Mode"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("dashboardDialog", "Swarm State"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("dashboardDialog", "Swarm Bhvr"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("dashboardDialog", "Link"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("dashboardDialog", "Batt"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("dashboardDialog", "GPS"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("dashboardDialog", "Mode"))
        self.btn_setSubswarm.setText(_translate("dashboardDialog", "                    Assign Selected UAVs to Subswarm:  "))
        self.lbl_selectSubswarm.setText(_translate("dashboardDialog", "Select Subswarm for Behavior Command:   "))
        self.btn_suspendSwarmBehavior.setText(_translate("dashboardDialog", "Suspend Swarm Behavior"))
        self.btn_beginSwarmBehavior.setText(_translate("dashboardDialog", "Begin Swarm Behavior"))
        self.swarm_label.setText(_translate("dashboardDialog", "Swarm Commands"))
        self.btn_egressSubswarm.setText(_translate("dashboardDialog", "                                                      Subswarm Egress:  "))
        self.btn_setSwarmState.setText(_translate("dashboardDialog", "                           Swarm State for Selected UAVs:  "))
        self.combo_swarmState.setItemText(0, _translate("dashboardDialog", "Preflight"))
        self.combo_swarmState.setItemText(1, _translate("dashboardDialog", "Flight Ready"))
        self.combo_swarmState.setItemText(2, _translate("dashboardDialog", "Ingress"))
        self.combo_swarmState.setItemText(3, _translate("dashboardDialog", "Swarm Ready"))
        self.combo_swarmState.setItemText(4, _translate("dashboardDialog", "Egress"))
        self.combo_swarmState.setItemText(5, _translate("dashboardDialog", "Landing"))
        self.label_overrides.setText(_translate("dashboardDialog", "Manual Overrides"))
        self.btn_AUTO.setText(_translate("dashboardDialog", "AUTO Selected UAVs"))
        self.btn_RTL.setText(_translate("dashboardDialog", "RTL Selected UAVs"))

