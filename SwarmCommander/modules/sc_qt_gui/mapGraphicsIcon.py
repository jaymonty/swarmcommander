#!/user/bin/env python3
"""
    Custom QGraphicsRectItem.  Creates a 1x1 Rectangle that can be scaled
    according to the map zoom level for Swarm Commander.

    Michael Day
    Dec 2014
"""

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPainterPath, QPen, QTransform
from PyQt5.QtCore import Qt

import math

class MapGraphicsIcon(QGraphicsRectItem):
    def __init__(self, id, label, parent = 0):
        QGraphicsRectItem.__init__(self, parent)
        #1x1 rectangle with top left at origin:
        self.setRect(0.0, 0.0, 1.0, 1.0)
        #shut off the outline:
        self.setPen(QPen(Qt.NoPen))

        self.__center_x = 0.0
        self.__center_y = 0.0
        self.__width = 1.0
        self.__height = 1.0

        self.__id = id

        self.__label = label
        self.__label_scale = 1.0

        #tooltips
        #self.setAcceptHoverEvents(True)
        #self.setToolTip(str(id))

    def textureIcon(self, file_pixmap):
        brush = QBrush(file_pixmap)

        self.mapTextureBasedOnZoom(brush)

    def mapTextureBasedOnZoom(self, brush):
        if brush.texture().width() > 0 and brush.texture().height() > 0:
            brush_trans = QTransform()
            brush_trans.translate(self.__center_x - self.__width * 0.5,
                    self.__center_y - self.__height * 0.5)
            brush_trans.scale(self.__width/float(brush.texture().width()),
                    self.__height/float(brush.texture().height()))
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
        
        self.centerIconAt(self.__center_x, self.__center_y)

        self.mapTextureBasedOnZoom(self.brush())

        self.__label_scale = sceneW / float(view.width()) * 1.5

    #note: not quite the same as the Qt-provided setPos method. This method sets
    #the icon's center at the given x, y.  Qt's setPos sets the upper left hand
    #corner
    def centerIconAt(self, x, y):
        self.__center_x = float(x)
        self.__center_y = float(y)
        topLeft_x = x - (self.__width * 0.5)
        topLeft_y = y - (self.__height * 0.5)
        self.setRect(topLeft_x, topLeft_y,
                self.__width, self.__height)

        self.__label.setPos(topLeft_x, topLeft_y)
        #self.__label.setPos(x, y)
        self.__label.setScale(self.__label_scale)

    def iconCenter(self):
        return (self.__center_x, self.__center_y)

    #heading is in radians
    def setHeading(self, heading):
        xForm = QTransform()
        xForm.translate(self.__center_x, self.__center_y)
        xForm.rotate(math.degrees(heading))
        xForm.translate(-self.__center_x, -self.__center_y)
        self.setTransform(xForm)
        
        self.mapTextureBasedOnZoom(self.brush())

    def getID(self):
        return self.__id

    #used for collision detection and mouse picking
    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
