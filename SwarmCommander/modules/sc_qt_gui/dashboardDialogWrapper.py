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
import math

# Mapping of swarm state numbers to readable names
# This is a hack until I can get the import from SwarmManager to work right
STATE_STRINGS = { 0: 'Preflight', \
                  1: 'Flight Ready', \
                  2: 'Launched', \
                  3: 'Swarming', \
                  4: 'Egressing', \
                  5: 'Landing', \
                  6: 'On Deck' }

#HACK (copying Duane's good idea above).  Mapping of mode IDs to names.
#TODO: this is probably a bad way to do this.  It's only a stopgap.
#Find a better way!
MODE_STRINGS = { 0:  'RTL', \
                 1:  'MANUAL', \
                 2:  'FBWA', \
                 3:  'GUIDED', \
                 4:  'AUTO', \
                 5:  'FBWB', \
                 6:  'CIRCLE', \
                 15: 'UNMAPPED' }
#UNMAPPED = ACRO, LOITER, INITIALIZING, TRAINING, STABILIZE, CRUISE

class DashboardDialog(QDialog):

    STAGING_WP_INDEX = 4
    EGRESS_WP_INDEX = 5
    RACETRACK_WP_INDEX = 7  # For now--this is just a racetrack waypoint

    # Temporary hard-code hack to maintain altitude separation
    uav_altitudes = {   4:375,
                        6:400,
                       11:425,
                        9:450,
                       12:475,
                        7:500,
                       10:525,
                       13:550,
                       14:575,
                       15:600,
                        5:625,
                      101:385,
                      102:410,
                      103:435,
                      104:460,
                      105:485,
                      106:510,
                      107:535,
                      108:560,
                      109:585,
                      110:610,
                      111:635 }

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
        self.__SWARM_STATE_COL = 3
        self.__LINK_COL = 4
        self.__BATT_REM_COL = 5
        self.__GPS_OK_COL = 6
        self.__MODE_COL = 7

        self.__dashboardUi.tableWidget.setColumnWidth(self.__ID_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__SUBSWARM_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__LINK_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__BATT_REM_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__GPS_OK_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__MODE_COL, 80)
        #end table stuff ------------------

        #slots
        self.__dashboardUi.btn_RTL.clicked.connect(self.rtl_button_pushed)
        self.__dashboardUi.btn_AUTO.clicked.connect(self.auto_button_pushed)
        self.__dashboardUi.btn_beginSwarmBehavior.clicked.connect(self.begin_swarm_behavior_pushed)
        self.__dashboardUi.btn_suspendSwarmBehavior.clicked.connect(self.suspend_swarm_behavior_pushed)
        self.__dashboardUi.btn_setSubswarm.clicked.connect(self.set_subswarm_pushed)
        self.__dashboardUi.btn_egressSubswarm.clicked.connect(self.egress_subswarm_pushed)

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
        self.__dashboardUi.tableWidget.setItem(row, self.__SWARM_STATE_COL, 
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__LINK_COL,
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__BATT_REM_COL,
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__GPS_OK_COL,
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__MODE_COL,
                QTableWidgetItem())

    def update_uav_row(self, id, uav_state):
        row = self.__uav_row_map[id]

        current_mode = 'ERROR'
        if uav_state['mode'] in MODE_STRINGS:
            current_mode = MODE_STRINGS[uav_state['mode']]

        self.__dashboardUi.tableWidget.item(row, self.__NAME_COL).setText(uav_state['name'])
        self.__dashboardUi.tableWidget.item(row, self.__BATT_REM_COL).setText(str(uav_state['batt_rem']))
        self.__dashboardUi.tableWidget.item(row, self.__MODE_COL).setText(current_mode)
        self.__dashboardUi.tableWidget.item(row, self.__SUBSWARM_COL).setText(str(uav_state['subswarm']))
        swarm_state = STATE_STRINGS[uav_state['swarm_state']]
        self.__dashboardUi.tableWidget.item(row, self.__SWARM_STATE_COL).setText(swarm_state)
        if (uav_state['gps_ok']):
            self.__dashboardUi.tableWidget.item(row, self.__GPS_OK_COL).\
                 setBackground(QBrush(QColor(0,255,0)))
        else:
            self.__dashboardUi.tableWidget.item(row, self.__GPS_OK_COL).\
                 setBackground(QBrush(QColor(255,0,0)))

        self.__uav_update_map[id] = time.clock()

    def rtl_button_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is None:
            print("No network module! (rtl_button_pushed)\n")
            return

        selected_uav_ids = self.selectTableUAVs()
        for selected_uav_id in selected_uav_ids:
            net_mod.change_mode_for(selected_uav_id, 0)


    def auto_button_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is None:
            print("No network module! (auto_button_pushed)\n")
            return
            
        selected_uav_ids = self.selectTableUAVs()
        for selected_uav_id in selected_uav_ids:
            net_mod.change_mode_for(selected_uav_id, 4)

#    def begin_swarm_behavior_pushed(self):
#        net_mod = self.sc_state.module('acs_network')
#        if net_mod is None:
#           print("No network module! (begin_swarm_behavior_pushed)\n")
#           return
#
#        selected_items = self.__dashboardUi.tableWidget.selectedItems()
#        selected_uav_ids = [ int(item.text()) for item in selected_items if (item.column() == self.__ID_COL) ]
#        for selected_uav_id in selected_uav_ids:
#            #TODO: "2" hard coded for "follow controller" needs to improve
#            net_mod.set_controller_for(selected_uav_id, 2)

    def set_subswarm_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is None:
            print("No network module! (set_subswarm_pushed)\n")
            return

        selected_items = self.__dashboardUi.tableWidget.selectedItems()
        selected_uav_ids = self.selectTableUAVs()
        selected_subswarm_id = int(self.__dashboardUi.spin_setSubswarm.value())
        for selected_uav_id in selected_uav_ids:
            net_mod.set_subswarm_for(selected_uav_id, selected_subswarm_id)

    def begin_swarm_behavior_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is None:
            print("No network module! (begin_swarm_behavior_pushed)\n")
            return


        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_selectSubswarm.value()))
        if subswarm_uavs == []: return  # Empty subswarm--nothing to do

        # Figure out who's in front
        lead_uav, lead_alt = 0, 0
        for uav in subswarm_uavs:
            if (DashboardDialog.uav_altitudes[uav] > lead_alt):
                lead_uav, lead_alt = uav, DashboardDialog.uav_altitudes[uav]

        # Send initialization (follower setup) commands
        for uav in subswarm_uavs:
            if uav == lead_uav:  # Send the lead UAV into the racetrack
                net_mod.set_controller_for(uav, 0)
                net_mod.set_waypoint_goto_for(uav, DashboardDialog.RACETRACK_WP_INDEX)

            if uav != lead_uav:
                net_mod.set_follower_params_for(uav, lead_uav, 25.0, math.pi, 0, \
                DashboardDialog.uav_altitudes[uav], 0)

        # Send activate commands
        for uav in subswarm_uavs:
            if uav == lead_uav:  # Send the lead UAV into the racetrack
                net_mod.set_controller_for(uav, 0)
                net_mod.set_waypoint_goto_for(uav, DashboardDialog.RACETRACK_WP_INDEX)

            else:  # Activate the follow controller for the rest
                net_mod.set_controller_for(uav, 2)

    def suspend_swarm_behavior_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is None:
            print("No network module! (suspend_swarm_behavior_pushed)\n")
            return

        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_selectSubswarm.value()))
        # Set the controller to 0 (autopilot only) and send UAV to the racetrack
        for uav_id in subswarm_uavs:
            net_mod.set_controller_for(uav_id, 0)
            net_mod.set_waypoint_goto_for(uav_id, DashboardDialog.STAGING_WP_INDEX)

    def egress_subswarm_pushed(self):
        net_mod = self.sc_state.module('acs_network')
        if net_mod is None:
            print("No network module! (egress_subswarm_pushed)\n")
            return

        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_egressSubswarm.value()))
        # Set the controller to 0 (autopilot only) and send UAV to the racetrack
        for uav_id in subswarm_uavs:
            net_mod.set_controller_for(uav_id, 0)
            net_mod.set_waypoint_goto_for(uav_id, DashboardDialog.EGRESS_WP_INDEX)

    def selectUAV(self, id):
        if id not in self.__uav_row_map:
            return

        rowNum = self.__uav_row_map[id]

        self.__dashboardUi.tableWidget.clearSelection()
        self.__dashboardUi.tableWidget.setCurrentCell(rowNum, self.__ID_COL,
                QItemSelectionModel.Select)

    def selectSubswarmUAVs(self, subswarm_id):
        result = []
        for vid in self.__uav_row_map:
            rowNum = self.__uav_row_map[vid]
            if (int(self.__dashboardUi.tableWidget.item(rowNum, self.__SUBSWARM_COL).text()) == subswarm_id):
                result.append(vid)
        return result

    def selectTableUAVs(self):
        selected_items = self.__dashboardUi.tableWidget.selectedItems()
        return [ int(item.text()) for item in selected_items if (item.column() == self.__ID_COL) ]


