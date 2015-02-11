"""
    Dashboard Dialog Wrapper.
    This class has all the run time functionality for the Ui_dashboardDialog.
    This class is edited by hand, while Ui_dashboardDialog is auto-generated
    by QDesigner.

    Michael Day
    Oct 2014
"""

from PyQt5.QtCore import QItemSelectionModel
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
        self.__SUBSWARM_COL = 2
        self.__LINK_COL = 3
        self.__BATT_REM_COL = 4
        self.__GPS_SATS_COL = 5
        self.__MODE_COL = 6

        self.__dashboardUi.tableWidget.setColumnWidth(self.__ID_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__SUBSWARM_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__LINK_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__BATT_REM_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__GPS_SATS_COL, 50)
        #end table stuff ------------------

        #slots
        self.__dashboardUi.btn_RTL.clicked.connect(self.rtl_button_pushed)
        self.__dashboardUi.btn_AUTO.clicked.connect(self.auto_button_pushed)
        self.__dashboardUi.btn_beginFollow.clicked.connect(self.begin_follow_pushed)
        self.__dashboardUi.btn_setSubswarm.clicked.connect(self.set_subswarm_pushed)

    def update_uav_states(self):
        for id in self.sc_state.uav_states.keys():
            if id not in self.__uav_row_map.keys():
                self.add_uav_to_dashboard(id)

        now = time.clock()

        for id, uav_state in self.sc_state.uav_states.items():
            if 'mode' not in uav_state.keys():
                #haven't got a FlightStatus message yet:
                continue

            if (self.__uav_update_map[id] < uav_state['last_status_update']):
                self.update_uav_row(id, uav_state)
                #link green
                self.__dashboardUi.tableWidget.item(self.__uav_row_map[id],
                    self.__LINK_COL).setBackground(QBrush(QColor(0,255,0)))
            elif now - uav_state['last_status_update'] > 10.0:
                #link red
                self.__dashboardUi.tableWidget.item(self.__uav_row_map[id],
                    self.__LINK_COL).setBackground(QBrush(QColor(255,0,0)))
            elif now - uav_state['last_status_update'] > 5.0:
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
        self.__uav_update_map[uav_id] = 0.0

        #__row_uav_map now needs a makeover
        self.__uav_row_map = {}
        for row_num in range(self.__dashboardUi.tableWidget.rowCount()):
            next_id = self.__dashboardUi.tableWidget.item(row_num,
                                                        self.__ID_COL)
            self.__uav_row_map[int(next_id.text())] = row_num

        self.init_row(uav_id)

    def init_row(self, id):
        row = self.__uav_row_map[id]        
        
        self.__dashboardUi.tableWidget.setItem(row, self.__NAME_COL, 
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__SUBSWARM_COL, 
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__LINK_COL,
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__BATT_REM_COL,
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__GPS_SATS_COL,
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__MODE_COL,
                QTableWidgetItem())

    def update_uav_row(self, id, uav_state):
        row = self.__uav_row_map[id]        

        self.__dashboardUi.tableWidget.item(row, self.__NAME_COL).setText(uav_state['name'])
        self.__dashboardUi.tableWidget.item(row, self.__BATT_REM_COL).setText(str(uav_state['batt_rem']))
        self.__dashboardUi.tableWidget.item(row, self.__GPS_SATS_COL).setText(str(uav_state['gps_sats']))
        self.__dashboardUi.tableWidget.item(row, self.__MODE_COL).setText(str(uav_state['mode']))
        self.__dashboardUi.tableWidget.item(row, self.__SUBSWARM_COL).setText(str(uav_state['subswarm']))

        self.__uav_update_map[id] = time.clock()

    def rtl_button_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is not None:
            net_mod.change_mode_all_aircraft(0)

    def auto_button_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is not None:
            net_mod.change_mode_all_aircraft(4)

    def begin_follow_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is not None:
            selected_items = self.__dashboardUi.tableWidget.selectedItems()
            selected_uav_ids = [ int(item.text()) for item in selected_items if (item.column() == self.__ID_COL) ]
            for selected_uav_id in selected_uav_ids:
            #TODO: "2" hard coded for "follow controller" needs to improve
                net_mod.set_controller_for(selected_uav_id, 2)

    def set_subswarm_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is not None:
            selected_items = self.__dashboardUi.tableWidget.selectedItems()
            selected_uav_ids = [ int(item.text()) for item in selected_items if (item.column() == self.__ID_COL) ]
            selected_subswarm_id = int(self.__dashboardUi.spin_setSubswarm.value())
            for selected_uav_id in selected_uav_ids:
                net_mod.set_subswarm_for(selected_uav_id, selected_subswarm_id)

    def selectUAV(self, id):
        if id not in self.__uav_row_map:
            return

        rowNum = self.__uav_row_map[id]

        self.__dashboardUi.tableWidget.clearSelection()
        self.__dashboardUi.tableWidget.setCurrentCell(rowNum, self.__ID_COL,
                QItemSelectionModel.Select)
