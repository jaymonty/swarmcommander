#!/usr/bin/env python3
'''
Swarm Commander - A Ground Control Station for oodles of aircraft.

Michael Day
Naval Postgraduate School 2014

Special Thanks to Andrew Tridgell and all the folks at diydrones.com
The design for this project is based on Tridgell's design of MAVProxy (another
excellent Ground Control Station), and depends greatly on and was influenced
by the work of the Open Source and Open Hardware Drone community.  At the danger
of leaving some people out we also thank:

The makers of ardupilot and ArduPlane for making their system open and allowing
so much learning.  Swarm Commander's first versions are aimed at that autopilot.

The developers and maintainers of the mavlink protocol and the PX4/Pixhawk for
their same spirit of openess.
'''

import sys, threading, time

from SwarmCommander.modules.lib import sc_state
from SwarmCommander.modules import sc_cli
from SwarmCommander.modules import sc_qt_gui

#Need this for using curses -- couldn't figure out how to put it in the module.
#Due to this decision:
#If ever I want a GUI-only Swarm Commander w/o a CLI I will probably need
#to make a new swarm_commander_gui.py file to replace the
#swarm_command.py file.
from curses import wrapper

#exit with message if we're not using Python 3:
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

#running cli in a separate thread:
class CLI_Thread(threading.Thread):
    def __init__(self, cli_mod, stdscr):
        threading.Thread.__init__(self)
        self.__cli_mod = cli_mod
        self.__stdscr = stdscr

    def run(self):
        self.__cli_mod.main_loop(self.__stdscr)

def main(stdscr):
    state = sc_state.SCState()
    state.initialize() #second init necessary to register callbacks
    cli_mod = sc_cli.SC_CLI_Module(state) 
    
    #First start CLI in its own thread
    cli_thread = CLI_Thread(cli_mod, stdscr)
    #makes the cli thread a daemon so that the cli will automatically
    #exit when the main thread (GUI thread) exits.
    cli_thread.setDaemon(True) 
    cli_thread.start()

    #load necessary modules---------
    state.load_module('map_tiler')
    #-----------------

    #Now start Qt application in main thread.  Note that Qt doesn't like being
    #run in any thread other than the main thread.
    qt_mod = sc_qt_gui.SC_QtGUIModule(state)
    qt_mod.start_app()

    #if the gui quits, we're outta here:
    state.unload_all_modules()
    #give the cli a chance to shutdown
    time.sleep(1)

wrapper(main)

#unload modules here as necessary.

#do any other cleanup here as necessary.

print("Your Swarm Commander Session has ended.\n")
