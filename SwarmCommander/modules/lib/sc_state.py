"""
    Swarm Commander State class.  
    
    Holds global state information for the entire application.
    A reference to the State class is passed to modules.
"""

from SwarmCommander.modules.lib import sc_module

class SCState(object):
    '''
    Contains state information intended to be passed between modules to give
    information about the state of the entire application.
    '''

    def __init__(self):
        self.__public_modules = {}

        #TODO: the rest of the state variables
    
    def module(self, name):
        ''' Find a public module. Return none if no module of that name, or if module is private. '''
        if name in self.public_modules:
            return self.public_modules[name]
        
        return None

    def add_public_module(self, name, mod):
        '''
        Append a public module to the dictionary of public modules
        Raises an exception if the module name alrady exists in the dictionary.
        '''

        if name in self.__public_modules:
            err_str = "Public Module " + name + " already exists"
            raise Exception (err_str)
            return

        if not isinstance(mod, sc_module.SCModule):
            err_str = "Cannot add module " + name + " as a Public module: it's not an SCModule"
            raise Exception (err_str)
            return

        self.__public_modules[name] = mod
            
