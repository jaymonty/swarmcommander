# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sequenceLandDialog.ui'
#
# Created: Mon Jun 15 14:22:19 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sequenceLandDialog(object):
    def setupUi(self, sequenceLandDialog):
        sequenceLandDialog.setObjectName("sequenceLandDialog")
        sequenceLandDialog.resize(224, 139)
        self.btnbx_CancelOK = QtWidgets.QDialogButtonBox(sequenceLandDialog)
        self.btnbx_CancelOK.setGeometry(QtCore.QRect(7, 100, 211, 27))
        self.btnbx_CancelOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnbx_CancelOK.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnbx_CancelOK.setCenterButtons(True)
        self.btnbx_CancelOK.setObjectName("btnbx_CancelOK")
        self.lbl_sequenceLanding = QtWidgets.QLabel(sequenceLandDialog)
        self.lbl_sequenceLanding.setGeometry(QtCore.QRect(7, 12, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_sequenceLanding.setFont(font)
        self.lbl_sequenceLanding.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_sequenceLanding.setWordWrap(True)
        self.lbl_sequenceLanding.setObjectName("lbl_sequenceLanding")
        self.combo_landOption = QtWidgets.QComboBox(sequenceLandDialog)
        self.combo_landOption.setGeometry(QtCore.QRect(27, 60, 171, 27))
        self.combo_landOption.setObjectName("combo_landOption")
        self.combo_landOption.addItem("")
        self.combo_landOption.addItem("")

        self.retranslateUi(sequenceLandDialog)
        self.btnbx_CancelOK.accepted.connect(sequenceLandDialog.accept)
        self.btnbx_CancelOK.rejected.connect(sequenceLandDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(sequenceLandDialog)

    def retranslateUi(self, sequenceLandDialog):
        _translate = QtCore.QCoreApplication.translate
        sequenceLandDialog.setWindowTitle(_translate("sequenceLandDialog", "Dialog"))
        self.btnbx_CancelOK.setToolTip(_translate("sequenceLandDialog", "<html><head/><body><p><br/></p></body></html>"))
        self.lbl_sequenceLanding.setText(_translate("sequenceLandDialog", "Swarm Sequence Landing Parameters"))
        self.combo_landOption.setToolTip(_translate("sequenceLandDialog", "<html><head/><body><p>Landing option (Runway 28 or 10 for westerly or easterly landing respectively)</p></body></html>"))
        self.combo_landOption.setItemText(0, _translate("sequenceLandDialog", "RW 28 (East to West)"))
        self.combo_landOption.setItemText(1, _translate("sequenceLandDialog", "RW 10 (West to East)"))

