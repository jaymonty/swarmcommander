#!/usr/bin/env python3
"""
    Swarm Commander Map Module
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

class SC_MapModule(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_MapModule, self).__init__(sc_state, "map", "map module")
        print("Booyah! Map loaded\n")

    def unload(self):
        pass

def init(sc_state):
    '''faciliates dynamic inialization of the module '''
    return SC_MapModule(sc_state)
