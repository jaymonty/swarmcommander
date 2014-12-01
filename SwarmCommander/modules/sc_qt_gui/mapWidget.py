# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapWidget.ui'
#
# Created: Mon Dec  1 14:21:03 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MapWidget(object):
    def setupUi(self, MapWidget):
        MapWidget.setObjectName("MapWidget")
        MapWidget.resize(852, 847)
        self.graphicsView = MapGraphicsView(MapWidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 821, 771))
        self.graphicsView.setObjectName("graphicsView")

        self.retranslateUi(MapWidget)
        QtCore.QMetaObject.connectSlotsByName(MapWidget)

    def retranslateUi(self, MapWidget):
        _translate = QtCore.QCoreApplication.translate
        MapWidget.setWindowTitle(_translate("MapWidget", "Form"))

from SwarmCommander.modules.sc_qt_gui.mapgraphicsview import MapGraphicsView
