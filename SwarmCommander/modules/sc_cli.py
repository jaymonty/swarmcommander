"""
    Swarm Commander Command Line Interface (CLI) module.
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

from atcommander import ATCommandSet

import curses, os, subprocess, traceback

class SC_CLI_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_CLI_Module, self).__init__(sc_state, "cli", "command line interface")
        self.time_to_quit = False
        self.stdscr = None

        self.__command_map = {
            'help'        : (self.cmd_help,    'List of Swarm Commander Commands'),
            'aircraft'    : (self.cmd_aircraft,'Aircraft commands'),
            'map'         : (self.cmd_map,     'Map commands'),
            'mavproxy'    : (self.cmd_mavproxy,'Start a MAVProxy instance'),
            'module'      : (self.cmd_module,  'Module commmands'),
            'network'     : (self.cmd_network, 'Network commands'),
            'quit'        : (self.cmd_quit,    'Exit Swarm Commander')
        }

    def unload(self):
        ''' Called when CLI module is unloaded '''
        self.time_to_quit = True

    def cmd_help(self, args):
        self.stdscr.addstr("Swarm Commander commands:\n")
        k = sorted(self.__command_map.keys())
        k.sort()
        for cmd in k:
            (fn, help) = self.__command_map[cmd]
            self.stdscr.addstr(cmd)
            self.stdscr.addstr(":")
            num_spaces = 16 - len(cmd)
            while num_spaces > 0:
                self.stdscr.addstr(" ")
                num_spaces = num_spaces - 1

            self.stdscr.addstr(help)
            self.stdscr.addstr("\n")

    def cmd_aircraft(self, args):
        '''"aircraft" command processing'''
        usage = "usage: aircraft <id|all> <arm|disarm|heartbeat|red_alert|status>\n"

        if len(args) < 2:
            self.stdscr.addstr(usage)
            return
        
        net_mod = self.sc_state.network
        plane_id = args[0]

        #list of aircraft ids to which this command applies
        aircraft = []
        if plane_id == "all":
            aircraft = self.sc_state.swarm_state.get_uav_ids()
        else:
            try:
                int_id = int(plane_id)
            except:
                self.stdscr.addstr("\tid arg must be an int or 'all'\n")
                return

            if int_id not in self.sc_state.swarm_state.uav_states.keys():
                self.stdscr.addstr("\tNo UAV with id: " +str(plane_id)+ "\n")
                return

            aircraft.append(int_id)

        if args[1] == "arm":
            for id in aircraft:
                net_mod.arm_throttle_for(id)
        elif args[1] == "disarm":
            if len(aircraft) > 1:
                self.stdscr.addstr("About to disarm multiple planes! SURE? (yes/N)\n")
                res = self.stdscr.getstr()
                decoded = res.decode("utf-8")
                if decoded.lower() != "yes":
                    self.stdscr.addstr("Aborted disarm.\n")
                    return
                else:
                    self.stdscr.addstr("Disarming multiple planes!!!\n")

            for id in aircraft:
                net_mod.arm_throttle_for(id, False)

        elif args[1] == "heartbeat":
            if len(args) < 3:
                self.stdscr.addstr("\tusage: aircraft <id|all> heartbeat <enable|disable>\n")
            elif args[2].lower() == "enable":
                for id in aircraft:
                    self.sc_state.network.set_autopilot_heartbeat_for(id, True)

            elif args[2].lower() == "disable":
                for id in aircraft:
                    self.sc_state.network.set_autopilot_heartbeat_for(id, False)

        elif args[1] == "red_alert":
            self.stdscr.addstr("About to kill throttle on those planes! SURE? (yes/N)\n")
            res = self.stdscr.getstr()
            decoded = res.decode("utf-8")
            if decoded.lower() != "yes":
                self.stdscr.addstr("Aborted red alert.\n")
                return
            else:
                self.stdscr.addstr("Killing throttle on those planes!!!\n")

        elif args[1] == "status":
            for id in aircraft:
                self.stdscr.addstr("UAV num " + str(id) + ":\n")
                self.stdscr.addstr(self.sc_state.swarm_state.uav_states[id].status_str())
                self.stdscr.addstr("\n")

        else:
            self.stdscr.addstr(usage)


    def cmd_map(self, args):
        '''"map" command processing'''
        usage = "usage: map <prefetch|show|hide|location>\n"

        #make sure we have the necessary modules loaded before trying these commands:
        if self.sc_state.module('map_tiler') is None:
            self.stdscr.addstr("Load map_tiler module first\n")
            return

        if len(args) < 1:
            self.stdscr.addstr(usage)
            return
        elif args[0] == "location":
            if len(args) < 3:
                self.stdscr.addstr("usage: map location lat lon <zoom>\n")
                return

            lat = float(args[1])
            lon = float(args[2])
            zoom = 15
            if len(args) >= 4:
                zoom = int(args[3])

            if self.sc_state.module('qt_gui') != None:
                self.sc_state.module('qt_gui').set_map_location(lat, lon, zoom)
            else:
                self.stdscr.addstr("Add qt_gui module first.\n")

        elif args[0] == "prefetch":
            #TODO: allow prefetching at an arbitrary location
            self.sc_state.module('map_tiler').prefetch() 
        else:
            self.stdscr.addstr(usage)

    def cmd_mavproxy(self, args):
        '''mavproxy startup command'''
        usage = "usage: mavproxy id <telem=False> <dev_path (only for telem)>\n"
        usage += "\tIf telem is False (default) use Wi-Fi link, otherwise use telem radio.\n"
        usage += "\tIf having trouble with Wi-Fi links, see network command.\n"

        radio_files = []
        plane_id = -1
        device = ""
        use_telem = False

        #get us some default radio device files
        try:
            radio_files = os.listdir('/dev/serial/by-id')
        except:
            radio_files = []

        if len(args) < 1:
            self.stdscr.addstr(usage)
            self.stdscr.addstr("Curently connected radios:\n")
            if len(radio_files) < 1:
                self.stdscr.addstr("   NONE\n")

            for next_radio in radio_files:
                self.stdscr.addstr("   " + next_radio + "\n")
            return
            
        plane_id = args[0]

        if len(args) > 1:
            if (args[1].lower() == "true" or args[1].lower() == "t"
                    or args[1].lower() == "1"):
                use_telem = True

        if len(args) > 0:
            if len(radio_files) < 1:
                if use_telem == True:
                    self.stdscr.addstr("No telem radio detected via USB.\n")
                    return
            else:    
                device = '/dev/serial/by-id/' + radio_files[0]
        
        if len(args) > 2:
            device = args[2]

        #if we made it here, all args have checked out

        if use_telem == False:
            self.sc_state.network.open_mavproxy_wifi(plane_id)

        else: #use_telem == True
            #setup SiK radio on proper channel
            try:
                atCmdr = ATCommandSet(device)
            except:
                self.stdscr.addstr("Cannot connect to: " + device + "\n")
                return
            self.stdscr.addstr("Radio: leaving cmd mode and unsticking...\n")
            atCmdr.leave_command_mode_force()
            atCmdr.unstick()

            if not atCmdr.enter_command_mode():
                self.stdscr.addstr("Can't enter cmd mode, can't set radio ID\n")
                return

            self.stdscr.addstr("Trying to set radio netid=" + plane_id + "\n")
        
            if not atCmdr.set_param(ATCommandSet.PARAM_NETID, plane_id):
                self.stdscr.addstr("Failed to set netid to " + plane_id + "\n")
                return

            self.stdscr.addstr("Writing params to radio EEPROM...\n")
            if not atCmdr.write_params():
                self.stdscr.addstr("Can't write params to telem radio EEPROM\n")
                return

            if not atCmdr.reboot():
                self.stdscr.addstr("Failed to reboot telem radio.\n")

            atCmdr.leave_command_mode()

            #fire up mavproxy with the appropriate device and args
            subprocess.Popen( ["/usr/bin/xterm", "-e", "mavproxy.py --baudrate 57600 --master " + device + " --speech --aircraft sc_" +  plane_id] )

    def cmd_module(self, args):
        '''"module" command processing'''
        usage = "usage: module <list|load|reload|unload>\n"

        if len(args) < 1:
            self.stdscr.addstr(usage)
            return
        elif args[0] == "list":
            for m in self.sc_state.get_all_available_modules():
                if m in self.sc_state.get_loaded_modules():
                    self.stdscr.addstr("* ")
                self.stdscr.addstr(m)
                self.stdscr.addstr("\n")
        elif args[0] == "load":
            if len(args) < 2:
                self.stdscr.addstr("usage: module load module_name\n")
                return
            try:
                self.sc_state.load_module(args[1])
            except Exception as e:
                self.stdscr.addstr(str(e))
                self.stdscr.addstr("\n")

        elif args[0] == "unload":
            if len(args) < 2:
                self.stdscr.addstr("usage: module unload module_name\n")
                return
            try:
                self.sc_state.unload_module(args[1])
            except Exception as e:
                self.stdscr.addstr(str(e))
                self.stdscr.addstr("\n")

        else:
            self.stdscr.addstr(usage)

    def cmd_network(self, args):
        '''network command processing'''
        usage = "usage: network <device|heartbeat|slave|status>\n"

        if len(args) < 1:
            self.stdscr.addstr(usage)
            return
        elif args[0] == "device":
            if len(args) < 2:
                self.stdscr.addstr("usage: network device device_name\n")
                self.stdscr.addstr("  e.g., eth0, wlan1, sitl_bridge\n")
                return
            self.sc_state.network.set_device(args[1])
        elif args[0] == "heartbeat":
            if len(args) < 2:
                self.stdscr.addstr("\tHeartbeat Enabled? " + str(self.sc_state.network.get_heartbeat_enabled()) + "\n")
                self.stdscr.addstr("\tTo enable/disable: network heartbeat <disable|enable>\n")
            elif args[1].lower() == "enable":
                self.sc_state.network.set_heartbeat_enabled(True)

            elif args[1].lower() == "disable":
                self.sc_state.network.set_heartbeat_enabled(False)

        elif args[0] == "status":
            self.stdscr.addstr("  Device: " + self.sc_state.network.get_device() + "\n")
            self.stdscr.addstr("    Heartbeats sent: " + str(self.sc_state.network.get_heartbeat_count()) + "\n")

        elif args[0] == "slave":
            if len(args) < 4:
                self.stdscr.addstr("usage: network slave <enable|disable> target_id port\n")
                return

            if args[1].lower() == "enable":
                self.sc_state.network.enable_slave(args[2], args[3])
            else:
                self.sc_state.network.disable_slave(args[2], args[3])
        else:
            self.stdscr.addstr(usage)

    def cmd_quit(self, args):
        self.cmd_module(["unload", "qt_gui"])
        self.time_to_quit = True

    def prepare_command(self, c_bytes):
        #turn curses command from bytes into string:
        c = c_bytes.decode("utf-8")

        c_tokens = c.split(" ")
        return c_tokens

    def process_command(self, c_tokens):
        ''' Process a command given by the user at the command line '''
        cmd = c_tokens[0]
        if (cmd == ""):
            return #nothing to do
        elif (cmd not in self.__command_map.keys()):
            self.stdscr.addstr("Unrecognized command\n")
        else:
            (fn, help) = self.__command_map[cmd]
            try:
                fn(c_tokens[1:])
            except Exception as e:
                print("ERROR in command: %s" % str(e))
                traceback.print_exc()

    def main_loop(self, stdscr):
        ''' called by external python program to start the main CLI loop '''
        self.stdscr = stdscr
        self.stdscr.scrollok(True)

        #I need to be able to see keyboard input
        curses.echo()

        while (not self.time_to_quit):
            stdscr.addstr("SwarmComm> ")
            stdscr.refresh()

            command = stdscr.getstr()
            c_tokens = self.prepare_command(command)
            cmd = c_tokens[0]
        
            self.process_command(c_tokens)

def init(sc_state):
    '''faciliates dynamic inialization of the module '''
    return SC_CLI_Module(sc_state)
