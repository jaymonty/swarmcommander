"""
    Swarm Commander Aerial Combat Swarms (ACS) network interface module
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

from ap_lib.acs_socket import Socket
from ap_lib import acs_messages

import threading, time

class SC_ACS_Network_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_ACS_Network_Module, self).__init__(sc_state, "acs_network", "ACS Network")

        #TODO: these parameters need to be less hard coded and also work with
        #more than SITL
        port = 5554
        #self.__device = 'eth0'
        #self.__device = 'sitl_bridge'
        self.__device = 'wlan1'
        my_ip = None
        bcast_ip = None

        try:
            self.__sock = Socket(0xff, port, self.__device, my_ip, bcast_ip)
        except Exception as e:
            print("Couldn't start up socket on interface %s", self.__device)

        self.__time_to_stop = False
        self.__t = threading.Thread(target=self.read_socket)
        self.__t.daemon = True
        self.__t.start()
   
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

    #TODO: finish this method -- not working yet
    def send_slave_msg(self, target_id, port, enable=True):
        ss = acs_messages.SlaveSetup()
        ss.msg_dst = int(target_id)
        ss.msg_secs = 0
        ss.msg_nsecs = 0
        ss.channel = 'udp:' + self.__sock.getIP() + ':' + str(port)
        #ss.channel = 'udp:127.0.0.1:' + str(port)
        ss.enable = enable

        print(ss.channel, "\n")

        #This message needs to make it through (set reliable flag)
        ss.msg_fl_rel = True
    
        self.__sock.send(ss)

    def enable_slave(self, target_id, port):
        self.send_slave_msg(target_id, port, True)

    def disable_slave(self, target_id, port):
        self.send_slave_msg(target_id, port, False)

    def set_device(self, device_name):
        print("TODO: implement set_device method after there is a close method in the acs_socket library class.\n")

def init(sc_state):
    '''facilitate dynamic initialization of the module '''
    return SC_ACS_Network_Module(sc_state)
