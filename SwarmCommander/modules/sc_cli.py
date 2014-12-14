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
        usage = "usage: mavproxy id <dev_path>\n"

        if len(args) < 1:
            self.stdscr.addstr(usage)
            return
        else:
            if len(args) < 2:
                try:
                    files = os.listdir('/dev/serial/by-id')
                except:
                    files = []

                if len(files) < 1:
                    self.stdscr.addstr("No radio detected connected via USB.\n")
                    return
                device = '/dev/serial/by-id/' + files[0]
            else:
                device = args[1]

            #setup SiK radio on proper channel
            atCmdr = ATCommandSet(device)
            self.stdscr.addstr("Radio: leaving command mode and unsticking...\n")
            atCmdr.leave_command_mode_force()
            atCmdr.unstick()

            if not atCmdr.enter_command_mode():
                self.stdscr.addstr("Unable to enter command mode, can't set radio ID\n")
                return

            self.stdscr.addstr("Trying to set radio to netid" + args[0] + "\n")
            if not atCmdr.set_param(ATCommandSet.PARAM_NETID, args[0]):
                self.stdscr.addstr("Failed to set netid to " + args[0] + "\n")
                return

            self.stdscr.addstr("Writing params to radio EEPROM...\n")
            if not atCmdr.write_params():
                print("Failed to write params to telem radio EEPROM\n")
                return

            if not atCmdr.reboot():
                print("Failed to reboot telem radio.\n")

            atCmdr.leave_command_mode()

            #fire up mavproxy with the appropriate device and args
            subprocess.Popen( ["/usr/bin/xterm", "-e", "mavproxy.py --baudrate 57600 --master " + device ] )
            #TODO: include proper mission # and sortie #


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
        usage = "usage: network <device|slave>\n"

        if self.sc_state.module('acs_network') is None:
            self.stdscr.addstr("Must load acs_network module before using network command.\n")
            return

        elif len(args) < 1:
            self.stdscr.addstr(usage)
            return
        elif args[0] == "device":
            if len(args) < 2:
                self.stdscr.addstr("usage: network device device_name\n")
                return
            self.sc_state.module('acs_network').set_device(args[1])
        elif args[0] == "slave":
            if len(args) < 4:
                self.stdscr.addstr("usage: network slave <enable|disable> target_id port\n")
                return

            if args[1].lower() == "enable":
                self.sc_state.module('acs_network').enable_slave(args[2], args[3])
            else:
                self.sc_state.module('acs_network').disable_slave(args[2], args[3])

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
