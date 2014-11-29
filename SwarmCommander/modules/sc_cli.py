"""
    Swarm Commander Command Line Interface (CLI) module.
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

import curses, traceback

class SC_CLI_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_CLI_Module, self).__init__(sc_state, "cli", "command line interface")
        self.time_to_quit = False
        self.stdscr = None

        self.__command_map = {
            'help'      : (self.cmd_help, 'List of Swarm Commander Commands'),
            'map'       : (self.cmd_map, 'Map commands'),
            'module'    : (self.cmd_module, 'Module commmands'),
            'quit'      : (self.cmd_quit, 'Exit Swarm Commander')
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
            self.stdscr.addstr(":\t\t")
            self.stdscr.addstr(help)
            self.stdscr.addstr("\n")

    def cmd_map(self, args):
        '''"map" command processing'''
        usage = "usage: map <prefetch|show|hide>\n"

        #make sure we have the necessary modules loaded before trying these commands:
        if self.sc_state.module('map_tiler') is None:
            self.stdscr.addstr("Load map_tiler module first\n")
            return

        if len(args) < 1:
            self.stdscr.addstr(usage)
            return
        elif args[0] == "prefetch":
            #TODO: allow prefetching at an arbitrary location
            self.sc_state.module('map_tiler').prefetch() 
        else:
            self.stdscr.addstr(usage)

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
                self.stdscr.addstr("usage: module load <module_name>\n")
                return
            try:
                self.sc_state.load_module(args[1])
            except Exception as e:
                self.stdscr.addstr(str(e))
                self.stdscr.addstr("\n")

        elif args[0] == "unload":
            if len(args) < 2:
                self.stdscr.addstr("usage: module unload <module_name>\n")
                return
            try:
                self.sc_state.unload_module(args[1])
            except Exception as e:
                self.stdscr.addstr(str(e))
                self.stdscr.addstr("\n")

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
