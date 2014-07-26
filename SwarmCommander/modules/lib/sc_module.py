'''SCModule is an abstract class that all Swarm Commander Modules should
   inherit from'''

import abc #support for Abstract Base Classes

class SCModule(object):
    __metaclass__ = abc.ABCMeta  #for abstract class

    '''
    Base class for all Swarm Commander modules
    '''

    def __init__(self, sc_state, name, description, public=False):
        '''
        Constructor

        if public is True then other modules can find this module with
        module('name')
        '''
        self.__sc_state = sc_state
        self.__name = name
        self.__description = description

        if public:
            sc_state.add_public_module(name, self)

    #methods defined as abstract must be implemented by inheriting class
    @abc.abstractmethod
    def unload(self):
        ''' Called when a module is unloaded. Used for cleanup. '''
        pass
 
    #methods not deinfed abstract _optionally_ implmented by ineriting classes
    def idle_task(self):
        ''' idle task will be called periodically'''
        pass

    def communication_packet(self, packet):
        '''handle a packet from serial or TCP/IP'''
        pass

    #properties return read only attributes (like a getter)
    @property
    def master(self):
        #TODO: do I want to do it this way?
        return self.__sc_state.master()

    @property
    def settings(self):
        #TODO: do I want to do it this way?
        return self.__sc_state.settings

    @property
    def sitl_output(self):
        #TODO: do I want to do it this way?
        return self.__sc_state.sitl_output

    @property
    def target_system(self):
        #TODO: do I want to do it this way?
        return self.__sc_state.status.target_system

    @property
    def target_component(self):
        #TODO: do I want to do it this way?
        return self.__sc_state.status.target_component

    @property
    def logdir(self):
        #TODO: do I want to do it this way?
        return self.__sc_state.status.logdir
    
    #these methods are not really meant to be implemented by inheriting classes,
    #but if they are their behavior is overriden.
    def module(self, name):
        '''Find a public module (will return None for private modules) '''
        return self.sc_state.module(name)

    def say (self, msg, prority='important'):
        return self.__sc_state.functions.say(msg)

