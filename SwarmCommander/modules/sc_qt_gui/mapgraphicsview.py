#!/usr/bin/env python3
"""
    Custom implementation of a QGraphicsView, MapGraphicsView.
    Allows custom event handling, among other custom behavior. Customizations
    are specific to the SwarmCommander application

    Michael Day
    Dec 2014
"""

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, pyqtSignal

import math

class MapGraphicsView(QGraphicsView):
    #signals
    just_zoomed = pyqtSignal(int)

    def __init__(self, parent = 0):
        QGraphicsView.__init__(self, parent)

        self.__current_zoom = 0
        self.__max_zoom = 20

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        #256 / 360 = 0.711111111
        #256 / 180 = 1.422222222
        #(tile size is 256 X 256)
        self.scale(0.71111111, 1.42222222)

    def mercatorYToLat(self, y):
        m_lat = math.atan(math.sinh(y))
        m_lat = math.degrees(m_lat)
        return m_lat

    def mercatorLatToY(self, lat):
        return math.asinh(math.tan(math.radians(lat)))

    #from my mapping into Mercator:
    def uniformLatToMercatorLat(self, lat):
                            #pi / 85.0 (85 degrees is top of map)
        mercator_y = lat * 0.036959913571644624
        m_lat = -self.mercatorYToLat(mercator_y)
        return m_lat

    #from Mercator into my mapping:
    def mercatorLatToUniformLat(self, lat):
        mercator_y = self.mercatorLatToY(lat)
        u_lat = mercator_y * (1.0 / 0.036959913571644624)
        return -u_lat

    def mouseReleaseEvent(self, event):
        sceneCoords = self.mapToScene(event.x(), event.y())

        lat = self.uniformLatToMercatorLat(sceneCoords.y())

        print("Scene coords: ", sceneCoords, "\n")
        print("Screen coords: (", event.x(), event.y(), ")\n")
        print("lat, lon: ", lat, sceneCoords.x(), "\n")

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

        print ("Current Zoom:", self.__current_zoom)
    
    def getCurrentZoom(self):
        return self.__current_zoom

    #TODO: fix; not working yet
    def zoomTo(self, lat, lon, zoom):
        delta_zoom = zoom - self.__current_zoom

        if self.__current_zoom + delta_zoom < 0 or self.__current_zoom + delta_zoom > self.__max_zoom or delta_zoom == 0:
            return

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

        self.centerOn(lon, self.mercatorLatToUniformLat(lat))

        self.__current_zoom = zoom

        self.just_zoomed.emit(self.__current_zoom)
