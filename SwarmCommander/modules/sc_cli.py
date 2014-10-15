"""
    Swarm Commander Command Line Interface (CLI) module.
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

import curses

class SC_CLI_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_CLI_Module, self).__init__(sc_state, "cli", "command line interface")
        self.time_to_quit = False
        self.stdscr = None

    def unload(self):
        ''' Called when CLI module is unloaded '''
        pass

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
        else:
            self.stdscr.addstr(usage)

    def process_command(self, c_bytes):
        ''' Process a command given by the user at the command line '''
        #turn curses command from bytes into string:
        c = c_bytes.decode("utf-8")

        c_tokens = c.split(" ")

        if c_tokens[0] == 'help':
            self.stdscr.addstr("Swarm Commander commands:\n")
            self.stdscr.addstr("help\n")
            self.stdscr.addstr("module\n")
            self.stdscr.addstr("quit\n")
        elif c_tokens[0] == 'module':
            self.cmd_module(c_tokens[1:])
        elif c_tokens[0] == 'quit':
            self.time_to_quit = True
        elif c_tokens[0] != '':
            self.stdscr.addstr("Unrecognized command\n")

    def main_loop(self, stdscr):
        ''' called by external python program to start the main CLI loop '''
        self.stdscr = stdscr

        #I need to be able to see keyboard input
        curses.echo()

        while (not self.time_to_quit):
            stdscr.addstr("SwarmComm> ")
            stdscr.refresh()

            command = stdscr.getstr()
        
            self.process_command(command)

def init(sc_state):
    '''faciliates dynamic inialization of the module '''
    return SC_CLI_Module(sc_state)
