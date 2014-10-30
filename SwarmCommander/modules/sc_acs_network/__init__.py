"""
    Swarm Commander Aerial Combat Swarms (ACS) network interface module
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

from ap_lib.acs_socket import Socket
from ap_lib import acs_messages

import threading

class SC_ACS_Network_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_ACS_Network_Module, self).__init__(sc_state, "acs_network", "ACS Network")

        #TODO: these parameters need to be less hard coded and also work with
        #more than SITL
        port = 5554
        device = 'sitl_bridge'
        my_ip = None
        bcast_ip = None

        try:
            self.__sock = Socket(0xff, port, device, my_ip, bcast_ip)
        except Exception as e:
            print("Couldn't start up socket on interface %s", device)

        self.__time_to_stop = False
        self.__t = threading.Thread(target=self.read_socket)
        self.__t.daemon = True
        self.__t.start()
   
    def process_flight_status(self, msg):
        name = msg.name

        #TODO: remove this workaround when we switch everthing to Python3:
        name = name[2:name.find("\\x00")]

        #print("%d %s %d %d" % (msg.msg_src, name, msg.armed, msg.mode))

        self.sc_state.update_uav_state(msg.msg_src, name)

    def read_socket(self):
        while not self.__time_to_stop:
            msg = self.__sock.recv()

            if msg is None:
                continue

            if isinstance(msg, acs_messages.FlightStatus):
                self.process_flight_status(msg)

    def unload(self):
        ''' Called when ACS Network modoule is unloaded'''
        #cleanup open sockets, shut down threads etc.

        self.__time_to_stop = True


def init(sc_state):
    '''facilitate dynamic initialization of the module '''
    return SC_ACS_Network_Module(sc_state)
