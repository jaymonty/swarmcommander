# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'greedyShooterDialog.ui'
#
# Created: Thu Nov  5 13:57:10 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_greedyShooterDialog(object):
    def setupUi(self, greedyShooterDialog):
        greedyShooterDialog.setObjectName("greedyShooterDialog")
        greedyShooterDialog.resize(224, 104)
        self.btnbx_CancelOK = QtWidgets.QDialogButtonBox(greedyShooterDialog)
        self.btnbx_CancelOK.setGeometry(QtCore.QRect(7, 60, 211, 27))
        self.btnbx_CancelOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnbx_CancelOK.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnbx_CancelOK.setCenterButtons(True)
        self.btnbx_CancelOK.setObjectName("btnbx_CancelOK")
        self.lbl_sequenceLanding = QtWidgets.QLabel(greedyShooterDialog)
        self.lbl_sequenceLanding.setGeometry(QtCore.QRect(7, 12, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_sequenceLanding.setFont(font)
        self.lbl_sequenceLanding.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sequenceLanding.setWordWrap(True)
        self.lbl_sequenceLanding.setObjectName("lbl_sequenceLanding")

        self.retranslateUi(greedyShooterDialog)
        self.btnbx_CancelOK.accepted.connect(greedyShooterDialog.accept)
        self.btnbx_CancelOK.rejected.connect(greedyShooterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(greedyShooterDialog)

    def retranslateUi(self, greedyShooterDialog):
        _translate = QtCore.QCoreApplication.translate
        greedyShooterDialog.setWindowTitle(_translate("greedyShooterDialog", "Dialog"))
        self.btnbx_CancelOK.setToolTip(_translate("greedyShooterDialog", "<html><head/><body><p><br/></p></body></html>"))
        self.lbl_sequenceLanding.setText(_translate("greedyShooterDialog", "Initiate Greedy Shooter Behavior"))

