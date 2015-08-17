#!/usr/bin/env python3
"""
    Swarm Commander Qt 5 GUI Module
    Cotainer module that holds all things GUI (for Qt interface to SC).
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QTimer
from acs_dashboards.lib.acs_general_gui.acs_map.mapWidgetWrapper import MapWidget
from SwarmCommander.modules.sc_qt_gui.dashboardDialogWrapper import DashboardDialog

import sys

class SC_QtGUIModule(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_QtGUIModule, self).__init__(sc_state, "qt_gui", "qt_gui module")
        self.__app = QApplication([])
        
        self.__mapWidget = MapWidget()

        self.__dashboardDialog = DashboardDialog(self.sc_state)
                                          
        self.__mapWidget.show()
        self.__dashboardDialog.show()

        #periodic updates...
        self.__updater = QTimer()
        self.__updater.setInterval(500)
        self.__updater.timeout.connect(self.time_to_update)
        self.__updater.start();

        #more frequent updates...
        self.__updaterFrequent = QTimer()
        self.__updaterFrequent.setInterval(40)
        self.__updaterFrequent.timeout.connect(self.time_to_update_frequent)
        self.__updaterFrequent.start();

        #zoom to default location:
        self.__mapWidget.zoomTo(16, 35.716888, -120.7646408)

        #slots
        self.__mapWidget.getView().just_selected_uav.connect(self.on_uav_select)

    def start_app(self):
        sys.exit(self.__app.exec_())

    def time_to_update_frequent(self):
        #update dashboard and map:
        self.__dashboardDialog.update_uav_states()

        #update icons on map
        for id, uav_state in self.sc_state.swarm_state.uav_states.items():
            self.__mapWidget.updateIcon(id, uav_state)

    def time_to_update(self):
        #check for new textures for the map:
        self.__mapWidget.checkForNewTextures()

    def unload(self):
        #do any cleanup here
        self.__mapWidget.done(0)
        self.__dashboardDialog.done(0)
        
        QApplication.quit()

    def on_uav_select(self, id):
        self.__dashboardDialog.selectUAV(id)

def init(sc_state):
    '''facilitates dynamic initialization of the module'''
    return SC_QtGUIModule(sc_state)
