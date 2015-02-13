"""
    Swarm Commander Aerial Combat Swarms (ACS) network interface module
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

from ap_lib.acs_socket import Socket
from ap_lib import acs_messages

import subprocess, threading, time

class SC_ACS_Network_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_ACS_Network_Module, self).__init__(sc_state, "acs_network", "ACS Network")

        self.__port = 5554
        self.__device = 'eth0'
        self.__my_ip = None
        self.__bcast_ip = None

        self.__sock = None
        self.open_socket()

        self.__time_to_stop = False
        self.__t = threading.Thread(target=self.read_socket)
        self.__t.daemon = True
        self.__t.start()
   
    def open_socket(self):
        try:
            self.__sock = Socket(0xff, self.__port, self.__device, self.__my_ip, self.__bcast_ip)
        except Exception as e:
            print("Couldn't start up socket on interface", self.__device)
            return

        # NOTE: The next two lines are *definitely* not the most pythonic
        #  (shouldn't just grab class data members)
        self.__my_ip = self.__sock._ip
        self.__bcast_ip = self.__sock._bcast

    def process_flight_status(self, msg):
        #print("%d %s %d %d" % (msg.msg_src, name, msg.armed, msg.mode))

        self.sc_state.update_uav_state(msg.msg_src, msg)

    def process_pose(self, msg):
        self.sc_state.update_uav_pose(msg.msg_src, msg)

    def read_socket(self):
        while not self.__time_to_stop:
            #give up the CPU for a bit
            #(0.002 secs -> about 500 Hz read rate in the worst case:
            #50 planes * 10 msgs/sec = 500 Hz
            time.sleep(0.002)

            #There is a minute chance somebody is trying to reopen the
            #socket in a different thread:
            if self.__sock == None:
                continue

            msg = self.__sock.recv()

            if msg is False:      # Saw a message, but not one we can use
                continue          # Check for more messages in queue
            if msg is None:       # No messages available in queue
                continue

            if isinstance(msg, acs_messages.FlightStatus):
                self.process_flight_status(msg)

            if isinstance(msg, acs_messages.Pose):
                self.process_pose(msg)

    def unload(self):
        ''' Called when ACS Network modoule is unloaded'''
        #cleanup open sockets, shut down threads etc.

        self.__time_to_stop = True

    def send_message_to(self, id, message):
        message.msg_dst = id
        cur_time = time.clock()
        message.msg_secs = int(cur_time)
        message.msg_nsecs = int(1e9 * (cur_time - int(cur_time)))
        
        res = None
        try:
            res = self.__sock.send(message)
        except Exception as ex:
            print (ex.args)
        return res

    #this method with arm or disarm (set arm_state to False to disarm)
    def arm_throttle_for(self, plane_id, arm_state=True):
        msg = acs_messages.Arm()
        msg.enable = arm_state
        msg.msg_fl_rel = True

        self.send_message_to(plane_id, msg)

    def change_mode_all_aircraft(self, mode):
        for id,name in self.sc_state.uav_states.items():
            message = acs_messages.Mode()
            message.mode = mode
            message.msg_fl_rel = True 

            self.send_message_to(id, message)

    def set_controller_for(self, id, controller):
        message = acs_messages.SetController()
        message.controller = controller
        message.msg_fl_rel = True

        self.send_message_to(id, message)

    def set_subswarm_for(self, id, subswarm):
        message = acs_messages.SetSubswarm()
        message.subswarm = subswarm
        message.msg_fl_rel = True
        self.send_message_to(id, message)

    def setup_mavlink_slave_ch(self, target_id, port, chan, enable=True):
        ''' Open/close a slave mavlink channel to the aircraft '''
        ss = acs_messages.SlaveSetup()
        ss.msg_dst = int(target_id)
        ss.msg_secs = 0
        ss.msg_nsecs = 0
        ss.channel = chan
        ss.enable = enable

        #This message needs to make it through (set reliable flag)
        ss.msg_fl_rel = True
    
        self.__sock.send(ss)

    def enable_slave(self, target_id, port, chan):
        self.setup_mavlink_slave_ch(target_id, port, True)

    def disable_slave(self, target_id, port, chan):
        self.setup_mavlink_slave_ch(target_id, port, False)

    def set_device(self, device_name):
        #shut off socket
        self.__sock = None

        self.__device = device_name

        #start socket on new device
        self.open_socket()

    def get_device(self):
        return self.__device

    def open_mavproxy_wifi(self, plane_id):
        #pick an aircraft-unique port
        slave_port = 15554 + int(plane_id)

        mavproxy_master = "udp:%s:%u" % (self.__my_ip, slave_port)
        self.enable_slave(plane_id, slave_port, mavproxy_master) 

        # Start up a MAVProxy instance and connect to slave channel
        subprocess.Popen( ["/usr/bin/xterm", "-e", "mavproxy.py --baudrate 57600 --master " + mavproxy_master + " --speech --aircraft sc_" +  plane_id] )

        #TODO: make it so I can shut off the slave channel when MAVProxy is
        #shut down (can't do it immediately or I lose MAVProxy prematurely)
        # Shut down slave channel
        #self.disable_slave(plane_id, slave_port, mavproxy_master)


def init(sc_state):
    '''facilitate dynamic initialization of the module '''
    return SC_ACS_Network_Module(sc_state)
