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
from SwarmCommander.modules.sc_qt_gui.mapDialog import Ui_mapDialog
from SwarmCommander.modules.sc_qt_gui.dashboardDialogWrapper import DashboardDialog

import sys

class SC_QtGUIModule(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_QtGUIModule, self).__init__(sc_state, "qt_gui", "qt_gui module")
        self.__app = QApplication([])
        
        self.__mapDialog = QDialog()
        self.__mapUi = Ui_mapDialog()
        self.__mapUi.setupUi(self.__mapDialog)

        self.__dashboardDialog = DashboardDialog(self.sc_state)
                                          
        #self.__mapDialog.show()
        self.__dashboardDialog.show()

        #periodic updates...
        self.__updater = QTimer()
        self.__updater.setInterval(500)
        self.__updater.timeout.connect(self.time_to_update)
        self.__updater.start();

    def start_app(self):
        sys.exit(self.__app.exec_())

    def end_app(self):
        QApplication.quit()

    def time_to_update(self):
        #update dashboard and map
        self.__dashboardDialog.update_uav_states()

    def unload(self):
        #do any cleanup here
        self.__mapDialog.done(0)
        self.__dashboardDialog.done(0)
        
        self.end_app()

def init(sc_state):
    '''facilitates dynamic initialization of the module'''
    return SC_QtGUIModule(sc_state)
