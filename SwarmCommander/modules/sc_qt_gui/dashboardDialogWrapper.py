"""
    Dashboard Dialog Wrapper.
    This class has all the run time functionality for the Ui_dashboardDialog.
    This class is edited by hand, while Ui_dashboardDialog is auto-generated
    by QDesigner.

    Michael Day
    Oct 2014
"""

from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5.QtGui import QBrush, QColor

from SwarmCommander.modules.sc_qt_gui.dashboardDialog import Ui_dashboardDialog
from SwarmCommander.modules.sc_qt_gui.behaviorDialogWrappers import SequenceLandDialog
from SwarmCommander.modules.sc_qt_gui.behaviorDialogWrappers import FixedFormationDialog
from SwarmCommander.modules.sc_qt_gui.behaviorDialogWrappers import SwarmSearchDialog
from ap_lib import ap_enumerations as enums
from ap_lib import bitmapped_bytes as bytes 

from acs_lib import acs_speech

import time
import math
import os

class DashboardDialog(QDialog):

    def __init__(self, sc_state):
        QDialog.__init__(self)

        self.sc_state = sc_state

        self.__speech = acs_speech.ACS_Speech()
        self.__speech.initialize('F') #female voice

        self.behavior_order = None # Container for swarm behavior order info

        self.__dashboardUi = Ui_dashboardDialog()
        self.__dashboardUi.setupUi(self)

        #table stuff ------------------------
        self.__dashboardUi.tableWidget.verticalHeader().setVisible(False)
        self.__dashboardUi.tableWidget.setSortingEnabled(False)

        #maps UAV ID to a table row number
        self.__uav_row_map = {}
        #maps UAV ID to the last time the table updated that ID
        self.__uav_update_map = {}

        self.__ID_COL = 0
        self.__NAME_COL = 1
        self.__SUBSWARM_COL = 2
        self.__SWARM_STATE_COL = 3
        self.__SWARM_BHVR_COL = 4
        self.__LINK_COL = 5
        self.__BATT_REM_COL = 6
        self.__GPS_OK_COL = 7
        self.__MODE_COL = 8

        self.__dashboardUi.tableWidget.setColumnWidth(self.__ID_COL, 40)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__NAME_COL, 80)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__SWARM_STATE_COL,100)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__SWARM_BHVR_COL, 110)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__SUBSWARM_COL, 50)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__LINK_COL, 40)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__BATT_REM_COL, 90)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__GPS_OK_COL, 35)
        self.__dashboardUi.tableWidget.setColumnWidth(self.__MODE_COL, 80)

        self.__dashboardUi.tableWidget.setColumnHidden(self.__LINK_COL, True)
        self.__dashboardUi.tableWidget.setColumnHidden(self.__GPS_OK_COL, True)
        self.__dashboardUi.tableWidget.setColumnHidden(self.__BATT_REM_COL, True)

        #sorting
        self.__current_sort_column = self.__ID_COL
        self.__current_sort_order = Qt.AscendingOrder

        #mutex
        self.__table_selection_being_updated = False
        #end table stuff ------------------

        #slots
        self.__dashboardUi.btn_RTL.clicked.connect(self.rtl_button_pushed)
        self.__dashboardUi.btn_AUTO.clicked.connect(self.auto_button_pushed)
        self.__dashboardUi.btn_beginSwarmBehavior.clicked.connect(self.begin_swarm_behavior_pushed)
        self.__dashboardUi.btn_suspendSwarmBehavior.clicked.connect(self.suspend_swarm_behavior_pushed)
        self.__dashboardUi.btn_pauseSwarmBehavior.clicked.connect(self.pause_swarm_behavior_pushed)
        self.__dashboardUi.btn_resumeSwarmBehavior.clicked.connect(self.resume_swarm_behavior_pushed)
        self.__dashboardUi.btn_setSubswarm.clicked.connect(self.set_subswarm_pushed)
        self.__dashboardUi.btn_egressSubswarm.clicked.connect(self.egress_subswarm_pushed)
        self.__dashboardUi.btn_setSwarmState.clicked.connect(self.set_swarm_state_pushed)

        self.__dashboardUi.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.table_header_dbl_clicked)
        self.__dashboardUi.tableWidget.itemSelectionChanged.connect(self.table_selectionChanged)

        self.__do_not_display_states = set()
        self.__do_not_display_states.add(enums.STATE_STRINGS[enums.PRE_FLIGHT])
        self.__do_not_display_states.add(enums.STATE_STRINGS[enums.FLIGHT_READY])
        self.__do_not_display_states.add(enums.STATE_STRINGS[enums.ON_DECK])
        self.__do_not_display_states.add(enums.STATE_STRINGS[enums.POST_FLIGHT])


    def __remap_uavs_to_rows(self):
        self.__uav_row_map = {}
        for row_num in range(self.__dashboardUi.tableWidget.rowCount()):
            next_item = self.__dashboardUi.tableWidget.item(row_num,
                                                        self.__ID_COL)
            self.__uav_row_map[next_item.data(Qt.DisplayRole)] = row_num

    def __run_sort(self):
        self.__dashboardUi.tableWidget.setSortingEnabled(True)
        self.__dashboardUi.tableWidget.sortItems(self.__current_sort_column, 
                self.__current_sort_order)
        self.__dashboardUi.tableWidget.setSortingEnabled(False)
        
        self.__remap_uavs_to_rows()

    def table_header_dbl_clicked(self, index): 
        #Already sorting on this index? Then swap order
        if index == self.__current_sort_column:
            if self.__current_sort_order == Qt.AscendingOrder:
                self.__current_sort_order = Qt.DescendingOrder
            else:
                self.__current_sort_order = Qt.AscendingOrder
        else:
            #always start with ascending
            self.__current_sort_order = Qt.AscendingOrder
        
        self.__current_sort_column = index

        self.__run_sort()
    
    #Ensure that the blue "selected" color doesn't cover up alert colors
    def table_selectionChanged(self):
        if self.__table_selection_being_updated is True:
            return

        rows_to_select = set()
        for next_item in self.__dashboardUi.tableWidget.selectedItems():
            rows_to_select.add(next_item.row())
            
        self.__table_selection_being_updated = True
        self.__dashboardUi.tableWidget.clearSelection()
        
        for i in rows_to_select:
            self.__dashboardUi.tableWidget.setRangeSelected(
                    QTableWidgetSelectionRange(i, self.__ID_COL, 
                        i, self.__NAME_COL), True)

        self.__table_selection_being_updated = False

    def update_uav_states(self):
        for id in self.sc_state.swarm_state.uav_states.keys():
            if id not in self.__uav_row_map.keys():
                self.add_uav_to_dashboard(id)

        now = time.time()

        for id, uav_state in self.sc_state.swarm_state.uav_states.items():
            if uav_state.get_mode() == -1:
                #haven't got a FlightStatus message yet:
                continue

            row = self.__uav_row_map[id]
            if (uav_state.get_last_status_update() == 0 or 
                self.__uav_update_map[id] < uav_state.get_last_status_update()):
                self.update_uav_row(id, uav_state)
                #link green
                self.__dashboardUi.tableWidget.item(row, self.__LINK_COL).\
                     setBackground(QBrush(QColor(0,255,0)))
            elif now - uav_state.get_last_status_update() > 10.0:
                #link red
                self.__dashboardUi.tableWidget.item(row, self.__LINK_COL).\
                     setBackground(QBrush(QColor(255,0,0)))
            elif now - uav_state.get_last_status_update() > 5.0:
                #link yellow
                self.__dashboardUi.tableWidget.item(row, self.__LINK_COL).\
                     setBackground(QBrush(QColor(255,255,0)))

            # Determine whether table row should be visible or hidden
            if (now - uav_state.get_last_status_update() > 60.0) or \
               (self.__dashboardUi.tableWidget.item(row, self.__SWARM_STATE_COL).text() \
                in self.__do_not_display_states):
                self.__dashboardUi.tableWidget.setRowHidden(row, True)
                self.sc_state.module("qt_gui").mapWidget.hideUAVIcon(id)
            else:
                self.__dashboardUi.tableWidget.setRowHidden(row, False)
                self.sc_state.module("qt_gui").mapWidget.showUAVIcon(id)

        self.__run_sort()

    def add_uav_to_dashboard(self, uav_id):
        #add a new table row
        self.__dashboardUi.tableWidget.insertRow(self.__dashboardUi.tableWidget.rowCount())
        next_item = QTableWidgetItem()
        #Sort ID column numerically, not lexicographically
        next_item.setData(Qt.DisplayRole, uav_id)
        self.__dashboardUi.tableWidget.setItem(
                self.__dashboardUi.tableWidget.rowCount() - 1,
                self.__ID_COL, next_item)

        #this row has never been updated
        self.__uav_update_map[uav_id] = 0.0
        self.__uav_row_map[uav_id] = self.__dashboardUi.tableWidget.rowCount()-1
        
        self.init_row(uav_id)

    def init_row(self, id):
        row = self.__uav_row_map[id]        
        
        self.__dashboardUi.tableWidget.setItem(row, self.__NAME_COL, 
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__SUBSWARM_COL, 
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__SWARM_STATE_COL, 
                QTableWidgetItem())
        self.__dashboardUi.tableWidget.setItem(row, self.__SWARM_BHVR_COL, 
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

        # Color code (and possibly aural warning) for unexpected autopilot modes
        if uav_state.get_mode() == enums.AUTO:
            self.__dashboardUi.tableWidget.item(row, self.__MODE_COL).\
                 setBackground(QBrush(QColor(255,255,255)))
        elif uav_state.get_mode() == enums.MANUAL:
            self.__dashboardUi.tableWidget.item(row, self.__MODE_COL).\
                 setBackground(QBrush(QColor(255,0,0)))

            #TODO; need a better "is_flying" alert than altitude:
            if uav_state.is_new_mode() and uav_state.get_alt_rel() > 20.0:
                self.__speech.say("MANUAL! on " + str(id))
        else:
            self.__dashboardUi.tableWidget.item(row, self.__MODE_COL).\
                 setBackground(QBrush(QColor(255,255,0)))

        #Color code for battery state
        if (uav_state.get_batt_vcc() > 10.8 and uav_state.get_batt_rem() > 40):
            self.__dashboardUi.tableWidget.item(row, self.__BATT_REM_COL).\
                 setBackground(QBrush(QColor(255,255,255)))
        elif (uav_state.get_batt_vcc() < 10.6 or uav_state.get_batt_rem() < 20):
            self.__dashboardUi.tableWidget.item(row, self.__BATT_REM_COL).\
                 setBackground(QBrush(QColor(255,0,0)))
        else: #voltage within 10.8 & 10.6 AND remaining curr within 20 & 40%
            self.__dashboardUi.tableWidget.item(row, self.__BATT_REM_COL).\
                 setBackground(QBrush(QColor(255,255,0)))

        self.__dashboardUi.tableWidget.item(row, self.__NAME_COL).setText(uav_state.get_name())
        self.__dashboardUi.tableWidget.item(row, self.__BATT_REM_COL).setText(
            '%.1f (%u%%)' % (uav_state.get_batt_vcc(),uav_state.get_batt_rem()))
        self.__dashboardUi.tableWidget.item(row, self.__MODE_COL).setText(uav_state.get_mode_str())

        #Sort SS_ID column numerically, not lexicographically
        ss_id_item = self.__dashboardUi.tableWidget.item(row, self.__SUBSWARM_COL)
        ss_id_item.setData(Qt.DisplayRole, uav_state.get_subswarm())

        self.__dashboardUi.tableWidget.item(row, self.__SWARM_STATE_COL).setText(uav_state.get_swarm_state_str())
        self.__dashboardUi.tableWidget.item(row, self.__SWARM_BHVR_COL).setText(uav_state.get_swarm_behavior_str())

        # Color code for GPS state
        if (uav_state.get_gps_ok()):
            self.__dashboardUi.tableWidget.item(row, self.__GPS_OK_COL).\
                 setBackground(QBrush(QColor(0,255,0)))
        else:
            self.__dashboardUi.tableWidget.item(row, self.__GPS_OK_COL).\
                 setBackground(QBrush(QColor(255,0,0)))

        self.__uav_update_map[id] = time.time()

    def rtl_button_pushed(self):
        net_mod = self.sc_state.network

        selected_uav_ids = self.selectTableUAVs()
        for selected_uav_id in selected_uav_ids:
            net_mod.change_mode_for(selected_uav_id, 0)

    def auto_button_pushed(self):
        net_mod = self.sc_state.network
            
        selected_uav_ids = self.selectTableUAVs()
        for selected_uav_id in selected_uav_ids:
            net_mod.change_mode_for(selected_uav_id, 4)

    def set_subswarm_pushed(self):
        net_mod = self.sc_state.network

        selected_items = self.__dashboardUi.tableWidget.selectedItems()
        selected_uav_ids = self.selectTableUAVs()
        selected_subswarm_id = int(self.__dashboardUi.spin_setSubswarm.value())
        for selected_uav_id in selected_uav_ids:
            net_mod.set_subswarm_for(selected_uav_id, selected_subswarm_id)

    def begin_swarm_behavior_pushed(self):
        net_mod = self.sc_state.network

        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_selectSubswarm.value()))
        if subswarm_uavs == []: return  # Empty subswarm--nothing to do

        selected_behavior = enums.SWARM_BHVR_VALUES[self.__dashboardUi.combo_swarmBehavior.currentText()]
        self.behavior_order = None

        if selected_behavior == enums.SWARM_LINEAR_FORMATION:
            dialog = FixedFormationDialog(self.sc_state, self)
            dialog.exec()
            if not self.behavior_order: return
            parser = bytes.LinearFormationOrderParser()
            parser.distance = self.behavior_order[0]
            parser.angle = self.behavior_order[1]
            parser.stack_formation = self.behavior_order[2]
            params = parser.pack()
            for uav in subswarm_uavs:
                net_mod.swarm_behavior_for(uav, enums.SWARM_LINEAR_FORMATION, params)

        elif selected_behavior == enums.SWARM_SEQUENCE_LAND:
            dialog = SequenceLandDialog(self.sc_state, self)
            dialog.exec()
            if not self.behavior_order: return
            parser = bytes.LandingOrderParser()
            parser.landing_wp_id = self.behavior_order
            params = parser.pack()
            for uav in subswarm_uavs:
                net_mod.swarm_behavior_for(uav, enums.SWARM_SEQUENCE_LAND, params)

        elif selected_behavior == enums.SWARM_SEARCH:
            dialog = SwarmSearchDialog(self.sc_state, self)
            dialog.exec()
            if not self.behavior_order: return
            parser = bytes.SearchOrderParser()
            parser.areaLength = self.behavior_order[0]
            parser.areaWidth = self.behavior_order[1]
            parser.lat = self.behavior_order[2]
            parser.lon = self.behavior_order[3]
            parser.masterID = self.behavior_order[4]
            parser.algorithmNumber = self.behavior_order[5]
            params = parser.pack()
            for uav in subswarm_uavs:
                net_mod.swarm_behavior_for(uav, enums.SWARM_SEARCH, params)

    def suspend_swarm_behavior_pushed(self):
        net_mod = self.sc_state.network

        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_selectSubswarm.value()))

        # Set the controller to 0 (autopilot only) and send UAV to the racetrack
        for uav_id in subswarm_uavs:
            net_mod.suspend_swarm_behavior_for(uav_id)  # Sets all aircraft to "swarm standby"

    def pause_swarm_behavior_pushed(self):
        self.set_swarm_behavior_pause(True)

    def resume_swarm_behavior_pushed(self):
        self.set_swarm_behavior_pause(False)

    def set_swarm_behavior_pause(self, pause_value):
        net_mod = self.sc_state.network

        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_selectSubswarm.value()))

        # Set the controller to 0 (autopilot only) and send UAV to the racetrack
        for uav_id in subswarm_uavs:
            net_mod.pause_swarm_behavior_for(uav_id, pause_value)  # Pause or resume any active behavior

    # Irrelevant button (placeholder for now), but might want to retain
    # the functionality and implement it differently on the payload side
    def egress_subswarm_pushed(self):
        pass
#        net_mod = self.sc_state.network
#
#        subswarm_uavs = self.selectSubswarmUAVs(int(self.__dashboardUi.spin_egressSubswarm.value()))
#        # Set the controller to 0 (autopilot only) and send UAV to the racetrack
#        for uav_id in subswarm_uavs:
#            net_mod.swarm_egress_for(uav_id)

    def set_swarm_state_pushed(self):
        net_mod = self.sc_state.network

        newState = self.__dashboardUi.combo_swarmState.currentText()
        selected_uav_ids = self.selectTableUAVs()
        for selected_uav_id in selected_uav_ids:
            net_mod.swarm_state_for(selected_uav_id, self.sc_state.swarm_state.uav_states[selected_uav_id].get_swarm_state_id_from_str(newState))

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

    def closeEvent(self, evt):
        self.sc_state.save_config()

        #call parent closeEvent method:
        QDialog.closeEvent(self, evt)
