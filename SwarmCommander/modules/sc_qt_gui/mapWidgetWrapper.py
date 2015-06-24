#!/user/bin/env python3
"""
    Wrapper for Ui_MapWidget class.  Ui_MapWidget is auto-generated from QtDesigner.
        This class exists to ensure custom functionality persists when the GUI
        widgets are modified with QtDesigner

    Michael Day
    Nov 2014
"""

from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsItemGroup
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QBrush, QTransform, QPen
from PyQt5.QtCore import Qt

from SwarmCommander.modules.sc_qt_gui.mapWidget import Ui_MapWidget
from SwarmCommander.modules.sc_qt_gui.mapGraphicsIcon import MapGraphicsIcon
from acs_lib import acs_math

from collections import OrderedDict

import pkg_resources, time, math

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
        
    def getView(self):
        return self.__view
    
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
    #depth applies to how many zoom levels (or detail layers) we have traveled
    #while attempting to get a lower resolution texture
    def textureRect(self, rect_tile):
        tile_info = rect_tile.data(0)

        if tile_info is None:
            return False

        pm = QPixmap(self.__tiler.tile_to_path(tile_info))  
        if pm.width() != 256:
            #print("Probably didn't get tile:", next_tile_info.x, next_tile_info.y, "\n")
            #TODO: Attempt to texture with a lower res tile
            #Bear in mind that you will have to take Mercator projection into
            #account on the lower res tile.
            
            #First Attempt: didn't work
            #if tile_info.zoom <= self.__tiler.get_min_zoom():
            #    return False
            #
            #find colocated lower res tile
            #(lat,lon) = tile_info.coord()
            #tile_info2 = self.__tiler.coord_to_tile(lat,lon, tile_info.zoom-1)
            #rect_tile.setData(0, tile_info2)
            #print("prev tile: ", tile_info.tile, tile_info.coord())
            #return self.textureRect(rect_tile, depth + 1)

            #until such time as we can pull lower res tiles and figure out
            #which area to render on a rectangle, skip:
            return False

        topLeft = rect_tile.boundingRect().topLeft()
        bottomRight = rect_tile.boundingRect().bottomRight()   
       
        width = bottomRight.x() - topLeft.x()
        height = bottomRight.y() - topLeft.y()

        brush_trans = QTransform()        
        brush_trans.translate(topLeft.x(), topLeft.y())
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
             
            #TODO: this code becomes applicable when lower res tiles become
            #available to higher zoom levels.
            #if self.__rect_tiles[key].data(0).zoom < self.__current_detail_layer:
                #lower res in there, try to get higher res 
                #(remove tile info of the lower res tile):
            #    del self.__rect_tiles[key]

    def updateIcons(self):
        for id, uav_state in self.sc_state.swarm_state.uav_states.items():
            if uav_state.get_lon() == 0.0:
                #haven't received a Pose message yet
                continue

            if id not in self.__plane_icons:
                #make the plane's label first
                label = QGraphicsTextItem(str(id), self.__plane_layer)
                label.setZValue(2)
                label.setDefaultTextColor(Qt.red)
                self.__plane_layer.addToGroup(label) 
                label.show()

                self.__plane_icons[id] = MapGraphicsIcon(id, label,
                        self.__plane_layer)
                self.__plane_icons[id].centerIconAt(uav_state.get_lon(),
                        -uav_state.get_lat())
                self.__plane_icons[id].textureIcon(self.__plane_icon_pixmap)

                #plane icons need to be drawn on top of map tiles:
                self.__plane_icons[id].setZValue(1)
                self.__plane_layer.addToGroup(self.__plane_icons[id])

                #key 0 = last update time
                self.__plane_icons[id].setData(0, 0)

                #refresh:
                #HACK: don't know why zooming works to refresh. Couldn't
                #get scene.invalidate() nor scene.update() to work
                self.onZoom(self.__current_detail_layer)
            
            now = time.clock()

            #if we don't have new pose data, then we don't update the plane icon
            if self.__plane_icons[id].data(0) is None or self.__plane_icons[id].data(0) >= uav_state.get_last_pose_update():
                continue

            #place icon
            self.__plane_icons[id].centerIconAt(uav_state.get_lon(), -uav_state.get_lat())
            #give correct heading:
            quat = uav_state.get_quat()
            heading = acs_math.yaw_from_quat(quat[0], quat[1], quat[2], quat[3])
            self.__plane_icons[id].setHeading(heading)
           
            #set last update time
            self.__plane_icons[id].setData(0, now)
     
    def zoomTo(self, zoomLevel, lat = 0, lon = 0):
        self.__view.zoomTo(zoomLevel, lat, lon)

    def onZoom(self, zoom_level):
        self.setCurrentDetailLayer(zoom_level)
        self.__mapWidgetUi.zoom_sb.setValue(zoom_level)
        for id, nextPlaneIcon in self.__plane_icons.items():
            nextPlaneIcon.scaleByViewAndTexture(self.__view)

    def onZoomSBValueChanged(self, new_zoom):
        if (int(self.__view.getCurrentZoom()) != new_zoom):
            self.__view.zoomTo(new_zoom)

    def onPan(self, new_lat, new_lon):
        lat_lon_str = str(new_lat) + ", " + str(new_lon) 
        self.__mapWidgetUi.coords_lb.setText(lat_lon_str)


