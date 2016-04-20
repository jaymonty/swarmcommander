# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interceptDialog.ui'
#
# Created: Thu Jan 28 10:41:35 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_interceptDialog(object):
    def setupUi(self, interceptDialog):
        interceptDialog.setObjectName("interceptDialog")
        interceptDialog.resize(228, 132)
        self.btnbx_CancelOK = QtWidgets.QDialogButtonBox(interceptDialog)
        self.btnbx_CancelOK.setGeometry(QtCore.QRect(7, 90, 211, 27))
        self.btnbx_CancelOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnbx_CancelOK.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnbx_CancelOK.setCenterButtons(True)
        self.btnbx_CancelOK.setObjectName("btnbx_CancelOK")
        self.lbl_TargetID = QtWidgets.QLabel(interceptDialog)
        self.lbl_TargetID.setGeometry(QtCore.QRect(7, 12, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_TargetID.setFont(font)
        self.lbl_TargetID.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_TargetID.setWordWrap(True)
        self.lbl_TargetID.setObjectName("lbl_TargetID")
        self.spinBox_TargetID = QtWidgets.QSpinBox(interceptDialog)
        self.spinBox_TargetID.setGeometry(QtCore.QRect(136, 50, 60, 27))
        self.spinBox_TargetID.setMinimum(1)
        self.spinBox_TargetID.setMaximum(200)
        self.spinBox_TargetID.setProperty("value", 101)
        self.spinBox_TargetID.setObjectName("spinBox_TargetID")
        self.label = QtWidgets.QLabel(interceptDialog)
        self.label.setGeometry(QtCore.QRect(60, 54, 71, 21))
        self.label.setObjectName("label")

        self.retranslateUi(interceptDialog)
        self.btnbx_CancelOK.accepted.connect(interceptDialog.accept)
        self.btnbx_CancelOK.rejected.connect(interceptDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(interceptDialog)

    def retranslateUi(self, interceptDialog):
        _translate = QtCore.QCoreApplication.translate
        interceptDialog.setWindowTitle(_translate("interceptDialog", "Dialog"))
        self.btnbx_CancelOK.setToolTip(_translate("interceptDialog", "<html><head/><body><p><br/></p></body></html>"))
        self.lbl_TargetID.setText(_translate("interceptDialog", "Intercept Parameters"))
        self.label.setText(_translate("interceptDialog", "Target ID"))

