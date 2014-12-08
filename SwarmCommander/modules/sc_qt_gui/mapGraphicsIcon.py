#!/user/bin/env python3
"""
    Custom QGraphicsRectItem.  Creates a 1x1 Rectangle that can be scaled
    according to the map zoom level for Swarm Commander.

    Michael Day
    Dec 2014
"""

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen, QTransform
from PyQt5.QtCore import Qt

import math

class MapGraphicsIcon(QGraphicsRectItem):
    def __init__(self, parent = 0):
        QGraphicsRectItem.__init__(self, parent)
        #1x1 rectangle with top left at origin:
        self.setRect(0.0, 0.0, 1.0, 1.0)
        #shut off the outline:
        self.setPen(QPen(Qt.NoPen))

        self.__width = 1.0
        self.__height = 1.0

    def textureIcon(self, file_pixmap):
        brush = QBrush(file_pixmap)

        if brush.texture().width() > 0 and brush.texture().height() > 0:
            brush_trans = QTransform()
            brush_trans.scale(1.0/float(brush.texture().width()),
                    1.0/float(brush.texture().height()))
            brush.setTransform(brush_trans)
    
        self.setBrush(brush)
    
    #Scales icon to the size indicated by the texture loaded onto it.
    #Therefore, if the texture set as the Brush for this MapGraphicsIcon is
    #32x32 pixels then the icon appears on the map as 32x32 no matter what
    #the zoom level
    def scaleByViewAndTexture(self, view):
        sceneCoordsTopLeft = view.mapToScene(0,0)
        sceneCoordsBottomRight = view.mapToScene(view.width(), view.height())

        sceneW = sceneCoordsBottomRight.x() - sceneCoordsTopLeft.x()
        sceneH = sceneCoordsBottomRight.y() - sceneCoordsTopLeft.y() 

        self.__width = sceneW / float(view.width()) * float(self.brush().texture().width())
        self.__height = sceneH / float(view.height()) * float(self.brush().texture().height())

        xForm = QTransform()
        xForm.scale(self.__width, self.__height)
        self.setTransform(xForm)
        
    #note: not quite the same as the Qt-provided setPos method. This method sets
    #the icon's center at the given x, y.  Qt's setPos sets the upper left hand
    #corner
    def centerIconAt(self, x, y):
        self.setPos(x - self.__width * 0.5, y - self.__height * 0.5)

    #heading is in radians
    def setHeading(self, heading):
        #xForm = QTransform(self.getTransform()
        self.setRotation(math.degrees(heading))
