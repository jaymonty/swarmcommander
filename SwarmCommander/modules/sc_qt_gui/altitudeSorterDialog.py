# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'altitudeSorterDialog.ui'
#
# Created: Mon Nov 30 17:34:10 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_altitudeSorterDialog(object):
    def setupUi(self, altitudeSorterDialog):
        altitudeSorterDialog.setObjectName("altitudeSorterDialog")
        altitudeSorterDialog.resize(224, 104)
        self.btnbx_CancelOK = QtWidgets.QDialogButtonBox(altitudeSorterDialog)
        self.btnbx_CancelOK.setGeometry(QtCore.QRect(7, 60, 211, 27))
        self.btnbx_CancelOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnbx_CancelOK.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnbx_CancelOK.setCenterButtons(True)
        self.btnbx_CancelOK.setObjectName("btnbx_CancelOK")
        self.lbl_altitudeSorter = QtWidgets.QLabel(altitudeSorterDialog)
        self.lbl_altitudeSorter.setGeometry(QtCore.QRect(7, 12, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_altitudeSorter.setFont(font)
        self.lbl_altitudeSorter.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_altitudeSorter.setWordWrap(True)
        self.lbl_altitudeSorter.setObjectName("lbl_altitudeSorter")

        self.retranslateUi(altitudeSorterDialog)
        self.btnbx_CancelOK.accepted.connect(altitudeSorterDialog.accept)
        self.btnbx_CancelOK.rejected.connect(altitudeSorterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(altitudeSorterDialog)

    def retranslateUi(self, altitudeSorterDialog):
        _translate = QtCore.QCoreApplication.translate
        altitudeSorterDialog.setWindowTitle(_translate("altitudeSorterDialog", "Dialog"))
        self.btnbx_CancelOK.setToolTip(_translate("altitudeSorterDialog", "<html><head/><body><p><br/></p></body></html>"))
        self.lbl_altitudeSorter.setText(_translate("altitudeSorterDialog", "Initiate Altitude Sorter Behavior"))

