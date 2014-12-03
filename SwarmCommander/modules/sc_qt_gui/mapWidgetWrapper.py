#!/user/bin/env python3
"""
    Wrapper for Ui_MapWidget class.  Ui_MapWidget is auto-generated from QtDesigner.
        This class exists to ensure custom functionality persists when the GUI
        widgets are modified with QtDesigner

    Michael Day
    Nov 2014
"""

from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsItemGroup
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QBrush, QTransform, QPen
from PyQt5.QtCore import Qt

from SwarmCommander.modules.sc_qt_gui.mapWidget import Ui_MapWidget

from collections import OrderedDict

class MapWidget(QDialog):
    def __init__(self, sc_state):
        QDialog.__init__(self)
    
        self.sc_state = sc_state

        self.__mapWidgetUi = Ui_MapWidget()
        self.__mapWidgetUi.setupUi(self)
        
        self.__view = self.__mapWidgetUi.graphicsView
        self.__scene = QGraphicsScene()
                
        self.__view.setScene(self.__scene)

        self.__current_lat = 35.720428
        self.__current_lon = -120.769924
        self.__current_ground_width = 41000000. #meters(start w/ view of whole earth)

        self.__tiler = sc_state.module("map_tiler")

        self.__current_detail_layer = 0 #corresponds to "zoom" in map_tiler module
        self.__detail_layers = []
        self.__rect_tiles = OrderedDict() #see rectKey method for how key works

        #detail layers are various levels of raster detail for the map.
        #0 is lowest level of detail, 20 highest.  0 loads fast and the 
        #entire world can fit on a single tile.  20 loads slow, and it is unwise
        #to try to show the entire world due to the number of tiles required 
        #(higher numbered detail layers are intended for "zooming in")
        self.setupDetailLayers()

        #slots
        self.__view.just_zoomed.connect(self.onZoom)

        #print("Attempting zoomTo\n")
        #self.__view.zoomTo(35.720428, -120.769924, 9)

    def rectKey(self, x, y):
        '''rect_tiles key'''
        return (self.__current_detail_layer, x, y)

    #returns (min_lat, max_lat, min_lon, max_lon) as a tuple
    def extentsOfVisibleWorld(self):
        topLeft = self.__view.mapToScene(0,0)
        bottomRight = self.__view.mapToScene(self.__view.width(), 
                                             self.__view.height())

        return (-topLeft.y(), -bottomRight.y(), topLeft.x(), bottomRight.x())

    def setupDetailLayers(self):
        #setup detail layers 0-20
        for i in range(0,21):
            self.__detail_layers.append(QGraphicsItemGroup())
            #add layer to scene:
            self.__scene.addItem(self.__detail_layers[i])            
            #hide all detail layers until it's time to show one:
            self.__detail_layers[i].hide()

        #show only the current detail layer
        self.setCurrentDetailLayer(0)

    def setCurrentDetailLayer(self, layerNum):
        self.__detail_layers[self.__current_detail_layer].hide()
        self.__detail_layers[layerNum].show()
        self.__current_detail_layer = layerNum

        self.__tiler.set_max_zoom(self.__current_detail_layer+1)
        #self.__tiler.prefetch()

        self.addTilesToCurrentDetailLayer()

    def addTilesToCurrentDetailLayer(self):
        pixel_width = self.__view.width()
        pixel_height = self.__view.height()

        (latTop, latBottom, lonLeft, lonRight) = self.extentsOfVisibleWorld()
        print("Extents:", latTop, latBottom, lonLeft, lonRight, "\n")
        tile_info_list = self.__tiler.area_to_tile_list_lat_lon(latTop, latBottom,
                lonLeft, lonRight, self.__current_detail_layer)

        for next_tile_info in tile_info_list:
            #if Rectangle already exists, don't create it again unless its
            #texture image is empty:
            key = self.rectKey(next_tile_info.x, next_tile_info.y)
            if key in self.__rect_tiles and self.__rect_tiles[key].brush().texture().width() != 0:
                continue
            
            factor = float(1<<self.__current_detail_layer)

            width = 360. / factor 
            height = 180. / factor

            x = -180. + width * next_tile_info.x
            y = -90. + height * next_tile_info.y

            #create rectangle for the TileInfo and put them into the scene
            self.__rect_tiles[key] = QGraphicsRectItem(x, y, width, height, self.__detail_layers[self.__current_detail_layer])
            #add raster data to the rect tile
            self.__tiler.load_tile(next_tile_info)
            #no border
            self.__rect_tiles[key].setPen(QPen(Qt.NoPen))       
            pm = QPixmap(self.__tiler.tile_to_path(next_tile_info))  
            if pm.width() != 256:
                #print("Probably didn't get tile:", next_tile_info.x, next_tile_info.y, "\n")
                #TODO: add this tile to a list to re-check for texture image later
                pass
           
            brush_trans = QTransform()
            brush_trans.translate(x, y)
            #TODO: deal with the hardcoded 256s (width and height of tiles)
            brush_trans.scale(width/256.0, height/256.0) 

            qb = QBrush(pm)
            qb.setTransform(brush_trans)
            self.__rect_tiles[key].setBrush(qb)
            
            #add rect tile to appropriate detail layer
            self.__detail_layers[self.__current_detail_layer].addToGroup(self.__rect_tiles[key])

    def onZoom(self, zoom_level):
        self.setCurrentDetailLayer(zoom_level)

