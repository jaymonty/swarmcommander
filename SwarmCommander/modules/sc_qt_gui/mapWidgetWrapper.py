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
from PyQt5.QtGui import QPixmap, QBrush, QTransform

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

    def rectKey(self, x, y):
        '''rect_tiles key'''
        return (self.__current_detail_layer, x, y)

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

        self.__tiler.set_max_zoom(self.__current_detail_layer)
        self.__tiler.prefetch()

        self.addTilesToCurrentDetailLayer()

    def addTilesToCurrentDetailLayer(self):
        pixel_width = self.__mapWidgetUi.graphicsView.width()
        pixel_height = self.__mapWidgetUi.graphicsView.height()

        print ("w, h: ", pixel_width, pixel_height, "\n")

        tile_info_list = self.__tiler.area_to_tile_list(self.__current_lat, self.__current_lon, self.__mapWidgetUi.graphicsView.width(), self.__mapWidgetUi.graphicsView.height(), self.__current_ground_width, self.__current_detail_layer)
       
        print (tile_info_list, ", len: ", len(tile_info_list), "\n")

        for next_tile_info in tile_info_list:
            #if Rectangle already exists, don't create it again unless its empty:
            key = self.rectKey(next_tile_info.x, next_tile_info.y)
            if key in self.__rect_tiles:
                continue
            
            factor = float(1<<self.__current_detail_layer)

            width = 360. / factor 
            height = 180. / factor

            x = -180. + width * next_tile_info.x
            y = 90. - height * next_tile_info.y

            #create rectangle for the TileInfo and put them into the scene
            self.__rect_tiles[key] = QGraphicsRectItem(x, y, width, height, self.__detail_layers[self.__current_detail_layer])
            #add raster data to the rect tile
            self.__tiler.load_tile(next_tile_info)
            pm = QPixmap(self.__tiler.tile_to_path(next_tile_info))
            print("Pixmap width: ", pm.width())
           
            brush_trans = QTransform()
            brush_trans.translate(x, y)
            #TODO: deal with the hardcoded 256s (width and height of tiles)
            brush_trans.scale(width/256.0, height/256.0) 

            qb = QBrush(pm)
            qb.setTransform(brush_trans)
            self.__rect_tiles[key].setBrush(qb)
            
            #add rect tile to appropriate detail layer
            self.__detail_layers[self.__current_detail_layer].addToGroup(self.__rect_tiles[key])

    def setView(self, lat, lon, zoom):
        """point the map at the appropriate location and zoom level"""
       
        #ensure that scene objects are available to look at at this location

        #convert lat/lon/zoom to x/y/z
        #(x,y) = self.sc_state.module("map_tiler").coord_to_pixel
        pass

