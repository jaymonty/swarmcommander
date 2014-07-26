"""
    Swarm Commander Command Line Interface (CLI) module.
"""
from SwarmCommander.modules.lib import sc_module

class SC_CLI_Module(sc_module.SCModule):
    def __init__(self, sc_state):
        super(SC_CLI_Module, self).__init__(sc_state, "cli", "command line interface", public=True)
        

    def unload(self):
        ''' Called when CLI module is unloaded '''
        pass

