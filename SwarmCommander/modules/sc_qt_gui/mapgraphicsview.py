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
    just_selected_uav = pyqtSignal(int)   

    def __init__(self, parent = 0):
        QGraphicsView.__init__(self, parent)

        self.__current_scale = 1.0
        self.__max_zoom = 20

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

    def getCurrentZoom(self):
        return math.log(self.__current_scale, 2)

    def getScaleFromZoom(self, zoom):
        return math.pow(2.0, zoom)

    def mouseReleaseEvent(self, event):
        #there must be a better way to pan, but this is quick:
        if event.button() == Qt.MidButton:
            if self.dragMode() == QGraphicsView.ScrollHandDrag:
                self.setDragMode(QGraphicsView.NoDrag)
            else:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            return #end of middle button stuff

        if event.button() == Qt.RightButton:
            return #right button done

        #assume left button if we got here

        sceneCoords = self.mapToScene(event.x(), event.y())

        #print("Scene coords: ", sceneCoords, "\n")
        #print("Screen coords: (", event.x(), event.y(), ")\n")

        #print(len(self.scene().items(sceneCoords)), "items at that pos:", sceneCoords, "\n")
        for nextItem in self.scene().items(sceneCoords, Qt.IntersectsItemShape):
            if "getID" in dir(nextItem):
                #print(nextItem, "ID: ", nextItem.getID(), "\n")
                #print(nextItem.boundingRect(), "\n")
                self.just_selected_uav.emit(nextItem.getID())

                #only do the first one under the mouse 
                #TODO: allow selecting more a different one
                break;

        #could have just been a drag:
        self.just_panned.emit(-sceneCoords.y(), sceneCoords.x())

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        
        if delta > 0:
            #self.zoom(2.0, event.x(), event.y())
            self.zoom(1.1, event.x(), event.y())
        else:
            #self.zoom(0.5, event.x(), event.y()) 
            self.zoom(1.0/1.1, event.x(), event.y()) 

    #s = amount to scale.  x, y in screen space (pixels)
    def zoom(self, s, x, y):
        sceneCoords = self.mapToScene(x,y)

        #make sure we're actually on the map before zooming:
        if sceneCoords.x() <= -180.0 or sceneCoords.x() >= 180.0 or sceneCoords.y() <= -90.0 or sceneCoords.y() >= 90.0:
            return

        self.__current_scale *= s

        #don't get too small
        if (self.__current_scale < 1.0):
            self.__current_scale /= s
            return

        #don't let tiles get too big
        if (self.getCurrentZoom() > self.__max_zoom + 1.0):
            self.__current_scale /= s
            return #no more zooming in
        
        self.scale(s, s)

        current_center = self.mapToScene(self.width() / 2, self.height() / 2)
        part_way = current_center;
        part_way.setX(part_way.x() - ((part_way.x() - sceneCoords.x()) / 8.0))
        part_way.setY(part_way.y() - ((part_way.y() - sceneCoords.y()) / 8.0))
        
        #move _slightly_ towards the point the mouse is centered on.
        #moving all the way too it proves too jarring for the user:
        self.centerOn(part_way)

        #signal anybody who wants to know about the zoom
        self.just_zoomed.emit(self.getCurrentZoom())

        #a zoom often results in a recentering of the view:
        self.just_panned.emit(-sceneCoords.y(), sceneCoords.x())

    def zoomTo(self, zoom, lat = None, lon = None):
        delta_zoom = zoom - self.getCurrentZoom()

        if self.getCurrentZoom() + delta_zoom < 0 or self.getCurrentZoom() + delta_zoom > self.__max_zoom or delta_zoom == 0:
            return

        delta_scale = self.getScaleFromZoom(delta_zoom)

        if lat == None or lon == None:
            centerCoords = self.mapToScene(self.width() * 0.5,
                    self.height() * 0.5)
            lat = -centerCoords.y()
            lon = centerCoords.x()

        self.zoom(delta_scale, self.width() / 2, self.height() / 2)

        self.centerOn(lon, -lat)

        self.just_zoomed.emit(self.getCurrentZoom())
        #a zoom often results in a recentering of the view:
        self.just_panned.emit(lat, lon)
