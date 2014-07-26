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

import sys

from SwarmCommander.modules.lib import sc_state
from SwarmCommander.modules import sc_cli

#exit with message if we're not using Python 3:
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

state = sc_state.SCState()

cli_mod = sc_cli.SC_CLI_Module(state)

print ("TODO: Swarm Commander. :)")

