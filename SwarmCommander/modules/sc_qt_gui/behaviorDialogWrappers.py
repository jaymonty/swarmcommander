"""
    Behavior Dialog Wrapper.
    This class has all the run time functionality for the swarm behavior
    popup dialog boxes.
    This class is edited by hand, while the individual dialog boxes
    (e.g., Ui_sequenceLandDialog.py) are auto-generated by QDesigner.

    Duane Davis (based on Michael Day's dashboardDialogWrapper pattern)
    June 2015
"""

from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5.QtGui import QBrush, QColor

from SwarmCommander.modules.sc_qt_gui.sequenceLandDialog import Ui_sequenceLandDialog
from SwarmCommander.modules.sc_qt_gui.fixedFormationDialog import Ui_fixedFormationDialog
import time
import math
import os


# Parent class for other behavior dialog boxes
class BehaviorDialog(QDialog):

    def __init__(self, sc_state, parent_dialog):
        QDialog.__init__(self)

        self.sc_state = sc_state
        self.parent = parent_dialog

    def cancelOk_btn_reject(self):
        self.parent.behavior_order = None
        self.close()


# Dialog box for entering user-defined parameters
# for the Swarm Sequenced Landing behavior
class SequenceLandDialog(BehaviorDialog):

    def __init__(self, sc_state, parent_dialog):
        BehaviorDialog.__init__(self, sc_state, parent_dialog)

        self.__sequencedLandUi = Ui_sequenceLandDialog()
        self.__sequencedLandUi.setupUi(self)

        #slots
        self.__sequencedLandUi.btnbx_CancelOK.accepted.connect(self.cancelOk_btn_accept)
        self.__sequencedLandUi.btnbx_CancelOK.rejected.connect(self.cancelOk_btn_reject)

    def cancelOk_btn_accept(self):
        ldn_wpt = None
        if self.__sequencedLandUi.combo_landOption.currentText() == "RW 28 (East to West)":
            lnd_wpt = 12
        elif self.__sequencedLandUi.combo_landOption.currentText() == "RW 10 (West to East)":
            lnd_wpt = 18
        self.parent.behavior_order = lnd_wpt
        self.close()


# Dialog box for entering user-defined parameters
# for the Fixed Formation behavior
class FixedFormationDialog(BehaviorDialog):

    def __init__(self, sc_state, parent_dialog):
        BehaviorDialog.__init__(self, sc_state, parent_dialog)

        self.__fixedFormationUi = Ui_fixedFormationDialog()
        self.__fixedFormationUi.setupUi(self)

        #slots
        self.__fixedFormationUi.btnbx_CancelOK.accepted.connect(self.cancelOk_btn_accept)
        self.__fixedFormationUi.btnbx_CancelOK.rejected.connect(self.cancelOk_btn_reject)

    def cancelOk_btn_accept(self):
        distance = self.__fixedFormationUi.spn_distance.value()
        angle = math.radians(self.__fixedFormationUi.spn_angle.value())
        stack = self.__fixedFormationUi.radio_stackFormation.isChecked()
        self.parent.behavior_order = ( distance, angle, stack )
        self.close()


