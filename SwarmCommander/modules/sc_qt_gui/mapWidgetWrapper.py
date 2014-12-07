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
from SwarmCommander.modules.sc_qt_gui.mapGraphicsIcon import MapGraphicsIcon

from collections import OrderedDict

import pkg_resources

class MapWidget(QDialog):
    def __init__(self, sc_state):
        QDialog.__init__(self)
    
        self.sc_state = sc_state

        self.__mapWidgetUi = Ui_MapWidget()
        self.__mapWidgetUi.setupUi(self)
        
        self.__view = self.__mapWidgetUi.graphicsView
        self.__view.setObjectName("SC_Map_View")
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

        self.__plane_layer = QGraphicsItemGroup()
        self.__scene.addItem(self.__plane_layer)
        self.__plane_icons = {}
        img_bytes = pkg_resources.resource_stream("SwarmCommander", "data/images/flyingWingTiny.png").read()
        self.__plane_icon_pixmap = QPixmap()
        self.__plane_icon_pixmap.loadFromData(img_bytes)

        #slots
        self.__view.just_zoomed.connect(self.onZoom)
        self.__mapWidgetUi.zoom_sb.valueChanged.connect(self.onZoomSBValueChanged)
        self.__view.just_panned.connect(self.onPan)
        
    def rectKey(self, x, y):
        '''rect_tiles key'''
        return (self.__current_detail_layer, x, y)

    #returns (min_lat, max_lat, min_lon, max_lon) as a tuple
    def extentsOfVisibleWorld(self):
        topLeft = self.__view.mapToScene(0,0)
        bottomRight = self.__view.mapToScene(self.__view.width(), 
                                             self.__view.height())

        return (-topLeft.y(), -bottomRight.y(), topLeft.x(), bottomRight.x())

    #returns a list of TileInfos that are currently visible
    def tilesInVisibleWorld(self):
        (latTop, latBottom, lonLeft, lonRight) = self.extentsOfVisibleWorld()
        #print("Extents:", latTop, latBottom, lonLeft, lonRight, "\n")
        tile_info_list = self.__tiler.area_to_tile_list_lat_lon(latTop, latBottom,
                lonLeft, lonRight, self.__current_detail_layer)

        return tile_info_list

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

    def createRectFromTileInfo(self, tile_info):
        #if Rectangle already exists, don't create it again
        key = self.rectKey(tile_info.x, tile_info.y)
        if key in self.__rect_tiles:
            return self.__rect_tiles[key]

        (y, x) = tile_info.coord()
        #TODO: do something about the hard coded 256s
        (end_y, end_x) = tile_info.coord((256, 256))
        
        #y values need to reflect across the equator due to the origin in scene space
        #being on the top right (as opposed to bottom left in tile space) 
        y = -y
        end_y = -end_y

        #keep things simple at the edges of the map:
        if y < -85.0:
            y = -85.0
        if end_y > 85.0:
            end_y = 85.0

        width = end_x - x
        height = end_y - y

        #create rectangle for the TileInfo and put it into the scene
        self.__rect_tiles[key] = QGraphicsRectItem(x, y, width, height, self.__detail_layers[self.__current_detail_layer])

        #add raster data to the rect tile
        self.__tiler.load_tile(tile_info)
        #no border
        self.__rect_tiles[key].setPen(QPen(Qt.NoPen))

        #remember the tiling data
        self.__rect_tiles[key].setData(0, tile_info)

        #attempt to add tile texture to rectangle:
        self.textureRect(self.__rect_tiles[key])

        return self.__rect_tiles[key]

    def addTilesToCurrentDetailLayer(self):
        tile_info_list = self.tilesInVisibleWorld()

        for next_tile_info in tile_info_list:
            next_rect = self.createRectFromTileInfo(next_tile_info)

            #add rect tile to appropriate detail layer
            self.__detail_layers[self.__current_detail_layer].addToGroup(next_rect)

    #returns True if texture successfully applied, False otherwise
    def textureRect(self, rect_tile):
        tile_info = rect_tile.data(0)

        pm = QPixmap(self.__tiler.tile_to_path(tile_info))  
        if pm.width() != 256:
            #print("Probably didn't get tile:", next_tile_info.x, next_tile_info.y, "\n")
            return False

        topLeft = rect_tile.boundingRect().topLeft()
        bottomRight = rect_tile.boundingRect().bottomRight()   

        brush_trans = QTransform()
        brush_trans.translate(topLeft.x(), topLeft.y())

        width = bottomRight.x() - topLeft.x()
        height = bottomRight.y() - topLeft.y()
        #TODO: deal with the hard coded 256s (width and height of tiles)
        brush_trans.scale(width/256.0, height/256.0)

        qb = QBrush(pm)
        qb.setTransform(brush_trans)
        rect_tile.setBrush(qb)
   
        return True

    def checkForNewTextures(self):
        #ONLY care about rects in the current view:
        tile_info_list = self.tilesInVisibleWorld()

        for next_tile_info in tile_info_list:
            key = self.rectKey(next_tile_info.x, next_tile_info.y)
            # make sure key exists in self.__rect_tiles
            if key not in self.__rect_tiles:
                self.createRectFromTileInfo(next_tile_info)
            
            if self.__rect_tiles[key].brush().texture().width() != 256:
                self.textureRect(self.__rect_tiles[key])
        
    def updateIcons(self):
        for id, uav_state in self.sc_state.uav_states.items():
            if id not in self.__plane_icons:
                self.__plane_icons[id] = MapGraphicsIcon(self.__plane_layer)
                brush = QBrush(self.__plane_icon_pixmap)

                if brush.texture().width() > 0 and brush.texture().height() > 0:
                    brush_trans = QTransform()
                    brush_trans.scale(1.0/float(brush.texture().width()),
                            1.0/float(brush.texture().height()))
                    brush.setTransform(brush_trans)
    
                self.__plane_icons[id].setBrush(brush)
                #plane icons need to be drawn on top of map tiles:
                self.__plane_icons[id].setZValue(1)
                self.__plane_layer.addToGroup(self.__plane_icons[id])

            if 'lon' not in uav_state.keys():
                #haven't received a Pose message yet
                continue

            self.__plane_icons[id].setPos(uav_state['lon'], -uav_state['lat'])
            #TODO: center icon on plane's position (only top left corner on the position desired)
            #self.__plane_icons[id].setOffset(-0.5, -0.5)
     
    def zoomTo(self, zoomLevel, lat = 0, lon = 0):
        self.__view.zoomTo(zoomLevel, lat, lon)

    def onZoom(self, zoom_level):
        self.setCurrentDetailLayer(zoom_level)
        self.__mapWidgetUi.zoom_sb.setValue(zoom_level)
        for id, nextPlaneIcon in self.__plane_icons.items():
            nextPlaneIcon.scaleByViewAndTexture(self.__view)

    def onZoomSBValueChanged(self, new_zoom):
        self.__view.zoomTo(new_zoom)

    def onPan(self, new_lat, new_lon):
        lat_lon_str = str(new_lat) + ", " + str(new_lon) 
        self.__mapWidgetUi.coords_lb.setText(lat_lon_str)
