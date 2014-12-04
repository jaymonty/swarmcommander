# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapWidget.ui'
#
# Created: Thu Dec  4 13:27:14 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MapWidget(object):
    def setupUi(self, MapWidget):
        MapWidget.setObjectName("MapWidget")
        MapWidget.resize(802, 703)
        self.graphicsView = MapGraphicsView(MapWidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 70, 800, 600))
        self.graphicsView.setObjectName("graphicsView")
        self.zoom_sb = QtWidgets.QSpinBox(MapWidget)
        self.zoom_sb.setGeometry(QtCore.QRect(70, 40, 46, 20))
        self.zoom_sb.setMaximum(20)
        self.zoom_sb.setObjectName("zoom_sb")
        self.zoom_lb = QtWidgets.QLabel(MapWidget)
        self.zoom_lb.setGeometry(QtCore.QRect(20, 40, 40, 20))
        self.zoom_lb.setObjectName("zoom_lb")
        self.coords_lb = QtWidgets.QLabel(MapWidget)
        self.coords_lb.setGeometry(QtCore.QRect(10, 680, 281, 17))
        self.coords_lb.setObjectName("coords_lb")

        self.retranslateUi(MapWidget)
        QtCore.QMetaObject.connectSlotsByName(MapWidget)

    def retranslateUi(self, MapWidget):
        _translate = QtCore.QCoreApplication.translate
        MapWidget.setWindowTitle(_translate("MapWidget", "Map"))
        self.zoom_lb.setText(_translate("MapWidget", "Zoom:"))
        self.coords_lb.setText(_translate("MapWidget", "Coords"))

from SwarmCommander.modules.sc_qt_gui.mapgraphicsview import MapGraphicsView
