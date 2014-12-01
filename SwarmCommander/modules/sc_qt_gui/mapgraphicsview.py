#!/usr/bin/env python3
"""
    Custom implementation of a QGraphicsView, MapGraphicsView.
    Allows custom event handling, among other custom behavior. Customizations
    are specific to the SwarmCommander application

    Michael Day
    Dec 2014
"""

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt

class MapGraphicsView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)

        self.__current_zoom = -1

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event):
        print(dir(event), "\n")
        print("X, Y:", event.x(), event.y(), "\n")

        delta = event.angleDelta().y()
        
        if delta > 0:
            self.zoom(2.0)
        else:
            self.zoom(0.5) 

    def zoom(self, s):
        if s > 1.0:
            self.__current_zoom = self.__current_zoom + 1.0
        else:
            if self.__current_zoom == -1:
                return #don't zoom out any farther
            self.__current_zoom = self.__current_zoom - 1.0
        
        self.scale(s, s)
