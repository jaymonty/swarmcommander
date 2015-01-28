# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapWidget.ui'
#
# Created: Tue Jan 27 16:44:25 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MapWidget(object):
    def setupUi(self, MapWidget):
        MapWidget.setObjectName("MapWidget")
        MapWidget.resize(792, 698)
        self.verticalLayout = QtWidgets.QVBoxLayout(MapWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.zoom_lb = QtWidgets.QLabel(MapWidget)
        self.zoom_lb.setObjectName("zoom_lb")
        self.verticalLayout.addWidget(self.zoom_lb)
        self.zoom_sb = QtWidgets.QSpinBox(MapWidget)
        self.zoom_sb.setMaximum(20)
        self.zoom_sb.setObjectName("zoom_sb")
        self.verticalLayout.addWidget(self.zoom_sb)
        self.graphicsView = MapGraphicsView(MapWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.coords_lb = QtWidgets.QLabel(MapWidget)
        self.coords_lb.setObjectName("coords_lb")
        self.verticalLayout.addWidget(self.coords_lb)

        self.retranslateUi(MapWidget)
        QtCore.QMetaObject.connectSlotsByName(MapWidget)

    def retranslateUi(self, MapWidget):
        _translate = QtCore.QCoreApplication.translate
        MapWidget.setWindowTitle(_translate("MapWidget", "Map"))
        self.zoom_lb.setText(_translate("MapWidget", "Zoom:"))
        self.coords_lb.setText(_translate("MapWidget", "Coords"))

from SwarmCommander.modules.sc_qt_gui.mapgraphicsview import MapGraphicsView
