# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fixedFormationDialog.ui'
#
# Created: Fri Jun 12 10:56:06 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fixedFormationDialog(object):
    def setupUi(self, fixedFormationDialog):
        fixedFormationDialog.setObjectName("fixedFormationDialog")
        fixedFormationDialog.resize(203, 199)
        self.btnbx_CancelOK = QtWidgets.QDialogButtonBox(fixedFormationDialog)
        self.btnbx_CancelOK.setGeometry(QtCore.QRect(10, 160, 181, 27))
        self.btnbx_CancelOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnbx_CancelOK.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnbx_CancelOK.setCenterButtons(True)
        self.btnbx_CancelOK.setObjectName("btnbx_CancelOK")
        self.lbl_fixedFormation = QtWidgets.QLabel(fixedFormationDialog)
        self.lbl_fixedFormation.setGeometry(QtCore.QRect(10, 12, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_fixedFormation.setFont(font)
        self.lbl_fixedFormation.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_fixedFormation.setWordWrap(True)
        self.lbl_fixedFormation.setObjectName("lbl_fixedFormation")
        self.radio_stackFormation = QtWidgets.QRadioButton(fixedFormationDialog)
        self.radio_stackFormation.setGeometry(QtCore.QRect(16, 128, 151, 22))
        self.radio_stackFormation.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.radio_stackFormation.setChecked(True)
        self.radio_stackFormation.setObjectName("radio_stackFormation")
        self.lbl_angle = QtWidgets.QLabel(fixedFormationDialog)
        self.lbl_angle.setGeometry(QtCore.QRect(41, 95, 61, 17))
        self.lbl_angle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_angle.setObjectName("lbl_angle")
        self.lbl_distance = QtWidgets.QLabel(fixedFormationDialog)
        self.lbl_distance.setGeometry(QtCore.QRect(31, 60, 71, 20))
        self.lbl_distance.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_distance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_distance.setObjectName("lbl_distance")
        self.spn_distance = QtWidgets.QSpinBox(fixedFormationDialog)
        self.spn_distance.setGeometry(QtCore.QRect(113, 57, 71, 27))
        self.spn_distance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spn_distance.setMaximum(500)
        self.spn_distance.setProperty("value", 25)
        self.spn_distance.setObjectName("spn_distance")
        self.spn_angle = QtWidgets.QSpinBox(fixedFormationDialog)
        self.spn_angle.setGeometry(QtCore.QRect(113, 90, 71, 27))
        self.spn_angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spn_angle.setMinimum(-179)
        self.spn_angle.setMaximum(180)
        self.spn_angle.setProperty("value", 180)
        self.spn_angle.setObjectName("spn_angle")

        self.retranslateUi(fixedFormationDialog)
        self.btnbx_CancelOK.accepted.connect(fixedFormationDialog.accept)
        self.btnbx_CancelOK.rejected.connect(fixedFormationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(fixedFormationDialog)

    def retranslateUi(self, fixedFormationDialog):
        _translate = QtCore.QCoreApplication.translate
        fixedFormationDialog.setWindowTitle(_translate("fixedFormationDialog", "Dialog"))
        self.btnbx_CancelOK.setToolTip(_translate("fixedFormationDialog", "<html><head/><body><p><br/></p></body></html>"))
        self.lbl_fixedFormation.setText(_translate("fixedFormationDialog", "Fixed Swarm Formation Parameters"))
        self.radio_stackFormation.setToolTip(_translate("fixedFormationDialog", "<html><head/><body><p>Select to have all aircraft in the same position relative to the leader</p></body></html>"))
        self.radio_stackFormation.setText(_translate("fixedFormationDialog", "Stack Formation"))
        self.lbl_angle.setToolTip(_translate("fixedFormationDialog", "<html><head/><body><p>Angle off the bow (degrees) of the commanded formation position</p></body></html>"))
        self.lbl_angle.setText(_translate("fixedFormationDialog", "Angle:"))
        self.lbl_distance.setToolTip(_translate("fixedFormationDialog", "<html><head/><body><p>Distance between aircraft (meters)</p></body></html>"))
        self.lbl_distance.setText(_translate("fixedFormationDialog", "Distance:"))
        self.spn_distance.setToolTip(_translate("fixedFormationDialog", "<html><head/><body><p>Distance between aircraft (meters)</p></body></html>"))
        self.spn_angle.setToolTip(_translate("fixedFormationDialog", "<html><head/><body><p>Angle off the bow (degrees) of the commanded formation position</p></body></html>"))

