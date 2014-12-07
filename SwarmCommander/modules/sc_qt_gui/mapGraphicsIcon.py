#!/user/bin/env python3
"""
    Custom QGraphicsRectItem.  Creates a 1x1 Rectangle that can be scaled
    according to the map zoom level for Swarm Commander.

    Michael Day
    Dec 2014
"""

from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPen, QTransform
from PyQt5.QtCore import Qt

class MapGraphicsIcon(QGraphicsRectItem):
    def __init__(self, parent = 0):
        QGraphicsRectItem.__init__(self, parent)
        #1x1 rectangle with top left at origin:
        self.setRect(0.0, 0.0, 1.0, 1.0)
        #shut off the outline:
        self.setPen(QPen(Qt.NoPen))
    
    #Scales icon to the size indicated by the texture loaded onto it.
    #Therefore, if the texture set as the Brush for this MapGraphicsIcon is
    #32x32 pixels then the icon appears on the map as 32x32 no matter what
    #the zoom level
    def scaleByViewAndTexture(self, view):
        sceneCoordsTopLeft = view.mapToScene(0,0)
        sceneCoordsBottomRight = view.mapToScene(view.width(), view.height())

        sceneW = sceneCoordsBottomRight.x() - sceneCoordsTopLeft.x()
        sceneH = sceneCoordsBottomRight.y() - sceneCoordsTopLeft.y() 

        desiredW = sceneW / float(view.width()) * float(self.brush().texture().width())
        desiredH = sceneH / float(view.height()) * float(self.brush().texture().height())

        xForm = QTransform()
        xForm.scale(desiredW, desiredH)
        self.setTransform(xForm)
        

