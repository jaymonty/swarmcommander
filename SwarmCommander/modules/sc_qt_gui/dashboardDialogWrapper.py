"""
    Dashboard Dialog Wrapper.
    This class has all the run time functionality for the Ui_dashboardDialog.
    This class is edited by hand, while Ui_dashboardDialog is auto-generated
    by QDesigner.

    Michael Day
    Oct 2014
"""

from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor

from SwarmCommander.modules.sc_qt_gui.dashboardDialog import Ui_dashboardDialog

import time

class DashboardDialog(QDialog):
    def __init__(self, sc_state):
        QDialog.__init__(self)

        self.sc_state = sc_state

        self.__dashboardUi = Ui_dashboardDialog()
        self.__dashboardUi.setupUi(self)

        #table stuff ------------------------
        self.__dashboardUi.tableWidget.verticalHeader().setVisible(False)

        #maps UAV ID to a table row number
        self.__uav_row_map = {}
        #maps UAV ID to the last time the table updated that ID
        self.__uav_update_map = {}

        self.__ID_COL = 0
        self.__NAME_COL = 1
        self.__LINK_COL = 2

    def update_uav_states(self):
        for id in self.sc_state.uav_states.keys():
            if id not in self.__uav_row_map.keys():
                self.add_uav_to_dashboard(id)

        now = int(time.time())

        for id, uav_state in self.sc_state.uav_states.items():
            if (self.__uav_update_map[id] < uav_state['last_update']):
                self.update_uav_row(id, uav_state['name'])
                #link green
                self.__dashboardUi.tableWidget.item(self.__uav_row_map[id],
                    self.__LINK_COL).setBackground(QBrush(QColor(0,255,0)))
            elif now - uav_state['last_update'] > 10:
                #link red
                self.__dashboardUi.tableWidget.item(self.__uav_row_map[id],
                    self.__LINK_COL).setBackground(QBrush(QColor(255,0,0)))
            elif now - uav_state['last_update'] > 5:
                #link yellow
                self.__dashboardUi.tableWidget.item(self.__uav_row_map[id],
                    self.__LINK_COL).setBackground(QBrush(QColor(255,255,0)))
            
                

    def add_uav_to_dashboard(self, uav_id):
        #add a new table row
        self.__dashboardUi.tableWidget.insertRow(self.__dashboardUi.tableWidget.rowCount())
        next_item = QTableWidgetItem()
        next_item.setText(str(uav_id))
        self.__dashboardUi.tableWidget.setItem(
                self.__dashboardUi.tableWidget.rowCount() - 1,
                self.__ID_COL, next_item)

        #sort as necessary (by ID):
        self.__dashboardUi.tableWidget.sortItems(self.__ID_COL);

        #this row has never been updated
        self.__uav_update_map[uav_id] = 0

        #__row_uav_map now needs a makeover
        self.__uav_row_map = {}
        for row_num in range(self.__dashboardUi.tableWidget.rowCount()):
            next_id = self.__dashboardUi.tableWidget.item(row_num,
                                                        self.__ID_COL)
            self.__uav_row_map[int(next_id.text())] = row_num

        self.init_row(uav_id)

    def init_row(self, id):
        name_item = QTableWidgetItem()
        link_item = QTableWidgetItem()
        
        row = self.__uav_row_map[id]        
        
        self.__dashboardUi.tableWidget.setItem(row, self.__NAME_COL, name_item)
        self.__dashboardUi.tableWidget.setItem(row, self.__LINK_COL, link_item)

    def update_uav_row(self, id, name):        
        row = self.__uav_row_map[id]        
        
        self.__dashboardUi.tableWidget.item(row, self.__NAME_COL).setText(name)

        self.__uav_update_map[id] = int(time.time())


