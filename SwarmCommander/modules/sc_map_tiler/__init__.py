#!/usr/bin/env python3
"""
    Swarm Commander Map Module
    Michael Day
    Oct 2014
"""
from SwarmCommander.modules.lib import sc_module

class SC_MapTilerModule(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_MapTilerModule, self).__init__(sc_state, "map_tiler", "map module")
        print("Booyah! Map Tiler loaded\n")

    def unload(self):
        pass


def init(sc_state):
    '''faciliates dynamic inialization of the module '''
    return SC_MapTilerModule(sc_state)
