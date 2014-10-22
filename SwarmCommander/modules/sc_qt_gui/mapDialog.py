# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapDialog.ui'
#
# Created: Thu Oct 16 08:22:25 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mapDialog(object):
    def setupUi(self, mapDialog):
        mapDialog.setObjectName("mapDialog")
        mapDialog.setWindowModality(QtCore.Qt.NonModal)
        mapDialog.resize(800, 600)

        self.retranslateUi(mapDialog)
        QtCore.QMetaObject.connectSlotsByName(mapDialog)

    def retranslateUi(self, mapDialog):
        _translate = QtCore.QCoreApplication.translate
        mapDialog.setWindowTitle(_translate("mapDialog", "Map"))

