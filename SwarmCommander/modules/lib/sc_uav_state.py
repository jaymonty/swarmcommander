"""
    Swarm Commander UAV State object.

    Encapsulates state information for a UAV.

    Author: Michael Day
    Date: Mar 2015
"""

import time

# Mapping of swarm state numbers to readable names
# This is a hack until I can get the import from SwarmManager to work right
STATE_STRINGS = { 0: 'Preflight', \
                  1: 'Flight Ready', \
                  2: 'Ingress', \
                  3: 'Swarm Ready', \
                  4: 'Swarm Active', \
                  5: 'Egress', \
                  6: 'Landing', \
                  7: 'On Deck' }

STATE_VALUES = { 'Preflight': 0, \
                 'Flight Ready': 1, \
                 'Ingress': 2, \
                 'Swarm Ready': 3, \
                 'Egress': 5, \
                 'Landing': 6 }

CTL_MODES = { 0: 'Autopilot', \
              1: 'Wpt Sequencer', \
              2: 'Follower' }

SWARM_BHVRS = {  0: 'Standby', \
                 1: 'Fixed Follow', \
                99: 'Egress' }

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

class UAVState(object):
    '''
    Contains state information for a single UAV.
    '''

    def __init__(self, id):
        #status variables
        self.__id = id
        self.__name = ""
        self.__mode = -1
        self.__batt_rem = 0
        self.__gps_ok = 0
        self.__swarm_state = 0
        self.__subswarm = 0
        self.__ctl_mode = 0
        self.__swarm_behavior = 0
        self.__last_status_update = 0.0 #last time SwarmCommander updated status
        self.__last_status_ts = 0.0     #last status message timestamp
        
        #pose variables
        self.__lat = 0.0
        self.__lon = 0.0
        self.__quat = (0.0, 0.0, 0.0, 0.0)
        self.__last_pose_update = 0.0   #last time SwarmCommander updated pose
        self.__last_pose_ts = 0.0       #last pose status timestamp

    def get_name(self):
        return self.__name

    def get_mode(self):
        return self.__mode

    def get_mode_str(self):
        current_mode = 'ERROR'
        try:
            current_mode = MODE_STRINGS[self.__mode]
        except:
            pass #failed to get mode string, assume bad index

        return current_mode

    def get_batt_rem(self):
        return self.__batt_rem

    def get_gps_ok(self):
        return self.__gps_ok

    def get_swarm_state(self):
        return self.__swarm_state

    def get_swarm_state_str(self):
        ret_val = 'ERROR'
        try:
            ret_val = STATE_STRINGS[self.__swarm_state]
        except:
            pass # failed to get state string, assume bad index

        return ret_val

    def get_swarm_state_id_from_str(self, state_str):
        ret_val = -1
        try:
            ret_val = STATE_VALUES[state_str]
        except:
            pass #failed to get state id, assume bad index

        return ret_val
    
    def get_subswarm(self):
        return self.__subswarm

    def get_ctl_mode(self):
        return self.__ctl_mode

    def get_ctl_mode_str(self):
        ret_val = 'ERROR'
        try:
            ret_val = CTL_MODES[self.__ctl_mode]
        except:
            pass # failed to get ctl mode string, assume bad index

        return ret_val

    def get_swarm_behavior(self):
        return self.__swarm_behavior

    def get_swarm_behavior_str(self):
        ret_val = 'ERROR'
        try:
            ret_val = SWARM_BHVRS[self.__swarm_behavior]
        except:
            pass #failed to get string, assume bad index

        return ret_val

    def get_last_status_update(self):
        return self.__last_status_update

    def get_last_status_ts(self):
        return self.__last_status_ts

    def get_lat(self):
        return self.__lat

    def get_lon(self):
        return self.__lon

    def get_quat(self):
        return self.__quat

    def get_last_pose_update(self):
        return self.__last_pose_update

    def get_last_pose_ts():
        return self.__last_pose_ts

    def status_str(self):
        stat_str = ""
        stat_str += "\tName:     " + self.get_name() + "\n"
        stat_str += "\tMode:     " + self.get_mode_str() + "\n"
        stat_str += "\tBatt:     " + str(self.get_batt_rem()) + "\n"
        stat_str += "\tGPS OK?   " + str(self.get_gps_ok()) + "\n"
        stat_str += "\tCtl Mode: " + str(self.get_ctl_mode_str()) + "\n"
        stat_str += "\tSubswarm: " + str(self.get_subswarm())
        stat_str += "\tSwarm State: " + self.get_swarm_state_str() 
        stat_str += "\tSwarm Behav: " + self.get_swarm_behavior_str() + "\n"

        return stat_str


    #There are no single-variable setters in this class ON PURPOSE.
    #I want variables to be set by network message only and all at once.
    
    def update_status(self, msg_timestamp, name, mode, batt_rem, gps_ok, swarm_state, subswarm, ctl_mode, swarm_behavior):
        #only want this message if it is newer than the previous one
        # -- need to look at message time stamp
        if (self.__last_status_ts > msg_timestamp):
            return

        self.__name = name
        self.__mode = mode
        self.__bat_rem = batt_rem
        self.__gps_ok = gps_ok
        self.__swarm_state = swarm_state
        self.__subswarm = subswarm
        self.__ctl_mode = ctl_mode
        self.__swarm_behavior = swarm_behavior

        self.last_status_ts = msg_timestamp
        self.last_status_update = time.clock()

    def update_pose(self, msg_timestamp, lat, lon, alt, quat):
        #only want this message if it is newer than the previous one
        # -- need to look at message time stamp
        if (self.__last_pose_ts > msg_timestamp):
            return

        self.__lat = lat
        self.__lon = lon
        self.__alt = alt
        self.__quat = quat

        self.__last_pose_ts = msg_timestamp
        self.__last_pose_update = time.clock()

