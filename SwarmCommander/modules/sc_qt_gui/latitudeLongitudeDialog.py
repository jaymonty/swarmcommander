# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'latitudeLongitudeDialog.ui'
#
# Created: Fri Jan 15 21:16:42 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_latitudeLongitudeDialog(object):
    def setupUi(self, latitudeLongitudeDialog):
        latitudeLongitudeDialog.setObjectName("latitudeLongitudeDialog")
        latitudeLongitudeDialog.resize(283, 163)
        self.btnbx_CancelOK = QtWidgets.QDialogButtonBox(latitudeLongitudeDialog)
        self.btnbx_CancelOK.setGeometry(QtCore.QRect(-110, 113, 341, 32))
        self.btnbx_CancelOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnbx_CancelOK.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnbx_CancelOK.setObjectName("btnbx_CancelOK")
        self.lbl_lat = QtWidgets.QLabel(latitudeLongitudeDialog)
        self.lbl_lat.setGeometry(QtCore.QRect(0, 43, 131, 20))
        self.lbl_lat.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_lat.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_lat.setObjectName("lbl_lat")
        self.lbl_lon = QtWidgets.QLabel(latitudeLongitudeDialog)
        self.lbl_lon.setGeometry(QtCore.QRect(0, 73, 131, 20))
        self.lbl_lon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_lon.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_lon.setObjectName("lbl_lon")
        self.doubleSpinBox_Lat = QtWidgets.QDoubleSpinBox(latitudeLongitudeDialog)
        self.doubleSpinBox_Lat.setGeometry(QtCore.QRect(150, 43, 111, 27))
        self.doubleSpinBox_Lat.setDecimals(6)
        self.doubleSpinBox_Lat.setMinimum(-90.0)
        self.doubleSpinBox_Lat.setMaximum(90.0)
        self.doubleSpinBox_Lat.setSingleStep(1e-06)
        self.doubleSpinBox_Lat.setProperty("value", 35.722118)
        self.doubleSpinBox_Lat.setObjectName("doubleSpinBox_Lat")
        self.doubleSpinBox_Lon = QtWidgets.QDoubleSpinBox(latitudeLongitudeDialog)
        self.doubleSpinBox_Lon.setGeometry(QtCore.QRect(150, 73, 111, 27))
        self.doubleSpinBox_Lon.setDecimals(6)
        self.doubleSpinBox_Lon.setMinimum(-180.0)
        self.doubleSpinBox_Lon.setMaximum(180.0)
        self.doubleSpinBox_Lon.setSingleStep(1e-06)
        self.doubleSpinBox_Lon.setProperty("value", -120.768539)
        self.doubleSpinBox_Lon.setObjectName("doubleSpinBox_Lon")
        self.lbl_latitudeLongitude = QtWidgets.QLabel(latitudeLongitudeDialog)
        self.lbl_latitudeLongitude.setGeometry(QtCore.QRect(30, 5, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_latitudeLongitude.setFont(font)
        self.lbl_latitudeLongitude.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_latitudeLongitude.setWordWrap(True)
        self.lbl_latitudeLongitude.setObjectName("lbl_latitudeLongitude")

        self.retranslateUi(latitudeLongitudeDialog)
        self.btnbx_CancelOK.accepted.connect(latitudeLongitudeDialog.accept)
        self.btnbx_CancelOK.rejected.connect(latitudeLongitudeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(latitudeLongitudeDialog)

    def retranslateUi(self, latitudeLongitudeDialog):
        _translate = QtCore.QCoreApplication.translate
        latitudeLongitudeDialog.setWindowTitle(_translate("latitudeLongitudeDialog", "Dialog"))
        self.lbl_lat.setToolTip(_translate("latitudeLongitudeDialog", "<html><head/><body><p>Latitude of the bottom point of search area</p></body></html>"))
        self.lbl_lat.setText(_translate("latitudeLongitudeDialog", "Latitude Order"))
        self.lbl_lon.setToolTip(_translate("latitudeLongitudeDialog", "<html><head/><body><p>Longitude of the bottom point of search area</p></body></html>"))
        self.lbl_lon.setText(_translate("latitudeLongitudeDialog", "Longitude Order"))
        self.lbl_latitudeLongitude.setText(_translate("latitudeLongitudeDialog", "Latitude/Longitude Order"))

