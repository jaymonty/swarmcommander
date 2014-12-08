#!/usr/bin/env python3
"""
    Custom implementation of a QGraphicsView, MapGraphicsView.
    Allows custom event handling, among other custom behavior. Customizations
    are specific to the SwarmCommander application

    Michael Day
    Dec 2014
"""

from PyQt5.QtWidgets import QApplication, QGraphicsView
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor

import math

class MapGraphicsView(QGraphicsView):
    #signals
    just_zoomed = pyqtSignal(int)
    just_panned = pyqtSignal(float, float)

    def __init__(self, parent = 0):
        QGraphicsView.__init__(self, parent)

        self.__current_zoom = 0
        self.__max_zoom = 20

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        #Hacking Qt: get rid of the stupid hand cursor
        #self.unsetCursor()
        #self.viewport().unsetCursor()
        QApplication.setOverrideCursor(Qt.ArrowCursor)

        #self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

    def mouseReleaseEvent(self, event):
        sceneCoords = self.mapToScene(event.x(), event.y())

        #print("Scene coords: ", sceneCoords, "\n")
        #print("Screen coords: (", event.x(), event.y(), ")\n")

        print(len(self.items(event.pos())), "items at that pos.\n")

        #could have just been a drag:
        self.just_panned.emit(-sceneCoords.y(), sceneCoords.x())

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        
        if delta > 0:
            self.zoom(2.0, event.x(), event.y())
        else:
            self.zoom(0.5, event.x(), event.y()) 

    #s = amount to scale.  x, y in screen space (pixels)
    def zoom(self, s, x, y):
        sceneCoords = self.mapToScene(x,y)

        #make sure we're actually on the map before zooming:
        if sceneCoords.x() <= -180.0 or sceneCoords.x() >= 180.0 or sceneCoords.y() <= -90.0 or sceneCoords.y() >= 90.0:
            return

        if s > 1.0:
            if self.__current_zoom == self.__max_zoom:
                return #no more zooming in
            self.__current_zoom = self.__current_zoom + 1.0
        else:
            if self.__current_zoom == 0:
                return #don't zoom out any farther
            self.__current_zoom = self.__current_zoom - 1.0
        
        self.scale(s, s)
        self.centerOn(sceneCoords)

        #signal anybody who wants to know about the zoom
        self.just_zoomed.emit(self.__current_zoom)
        #a zoom often results in a recentering of the view:
        self.just_panned.emit(-sceneCoords.y(), sceneCoords.x())

    def getCurrentZoom(self):
        return self.__current_zoom

    def zoomTo(self, zoom, lat = None, lon = None):
        delta_zoom = zoom - self.__current_zoom

        if self.__current_zoom + delta_zoom < 0 or self.__current_zoom + delta_zoom > self.__max_zoom or delta_zoom == 0:
            return

        if lat == None or lon == None:
            centerCoords = self.mapToScene(self.width() * 0.5,
                    self.height() * 0.5)
            lat = -centerCoords.y()
            lon = centerCoords.x()

        s = 1.0
        if delta_zoom > 0:
            s = 2.0# * delta_zoom
        else:
            s = 0.5# / delta_zoom

        abs_delta_zoom = math.fabs(delta_zoom)
        while abs_delta_zoom > 0:
            #self.centerOn(lon, lat)
            self.scale(s,s)
            abs_delta_zoom = abs_delta_zoom - 1

        self.centerOn(lon, -lat)

        self.__current_zoom = zoom

        self.just_zoomed.emit(self.__current_zoom)
        #a zoom often results in a recentering of the view:
        self.just_panned.emit(lat, lon)
