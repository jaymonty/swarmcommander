"""
    Swarm Commander State Module.  
    
    Holds global state information for the entire application.
    A reference to the State class is passed to modules.
"""

from SwarmCommander.modules.lib import sc_module
from SwarmCommander.modules.lib import sc_uav_state

import sys, pip, traceback, zipfile, zipimport, time

class SCState(object):
    '''
    Contains state information intended to be passed between modules to give
    information about the state of the entire application.
    '''

    def __init__(self):
        #module state
        self.__loaded_modules = {}
        self.__module_path = 'SwarmCommander.modules.sc_'

        #Dictionary of UAVState classes that hold each UAV's state
        self.uav_states = {}

        #modules wanting UAV updates
        self.__modules_wanting_uav_updates = []

    def update_uav_preprocess_msg(self, id, msg):
        if id not in self.uav_states:
            self.uav_states[id] = sc_uav_state.UAVState(id)

        #TODO: process header

    def update_uav_state(self, id, msg):
        self.update_uav_preprocess_msg(id, msg)
    
        #TODO: verify this is a FlightStatus message
        
        name = msg.name

        #TODO: remove this workaround when we switch everthing to Python3:
        name = name[2:name.find("\\x00")]

        self.uav_states[id].update_status(msg.msg_secs, name, msg.mode, msg.batt_rem, msg.batt_vcc, msg.ok_gps, msg.swarm_state, msg.msg_sub, msg.ctl_mode, msg.swarm_behavior)

    def update_uav_pose(self, id, msg):
        self.update_uav_preprocess_msg(id, msg)

        quat = (msg.q_x, msg.q_y, msg.q_z, msg.q_w)
        self.uav_states[id].update_pose(msg.msg_secs, msg.lat, msg.lon, msg.alt, quat)

    def get_uav_ids(self):
        ids = []
        for id in self.uav_states.keys():
            ids.append(id)

        return ids

    def module(self, name):
        ''' Find a loaded module. Return none if no loaded module of that name, or if module is private. '''
        if name in self.__loaded_modules:
            return self.__loaded_modules[name]
        
        return None

    def get_loaded_modules(self):
        return self.__loaded_modules

    def get_all_available_modules(self):
        file_list = []

        sc_path = ""
        installed_packages = pip.get_installed_distributions()
        for next_pack in installed_packages:
            if next_pack.key == 'swarmcommander':
                sc_path = next_pack.location
                break;

        if sc_path == "":
            print("Couldn't find where pip installed swarmcommander.")
            return file_list

        zf = zipfile.ZipFile(sc_path, 'r')

        for next_file in zf.namelist():
            if next_file.startswith("SwarmCommander/modules/sc_") and not next_file.endswith(".pyc"):
                next_module = next_file.replace("SwarmCommander/modules/sc_","")
                next_module = next_module.replace(".py","")
                if next_module.rfind("/") != -1:
                    next_module = next_module[0:next_module.rfind("/")]
                if next_module not in file_list:
                    file_list.append(next_module)

        return file_list        

    def get_module_full_path(self, module_name):
        modpath = '%s%s' % (self.__module_path, module_name)
        return modpath

    def unload_module(self, module_name):
        ''' Attemp to unload a module.  Throws an exception if unable to unload the module '''

        mod = self.module(module_name)

        if mod == None:
            raise Exception('Module not loaded')
            return

        if hasattr(mod, 'unload'):
            mod.unload()
        else:
            raise Exception('Module has no unload method')
            return

        #Removes the module from the dictionary of loaded modules
        del self.__loaded_modules[module_name]

    def unload_all_modules(self): 
        for name,module in self.__loaded_modules.items():
            self.unload_module(name)

    def load_module(self, module_name):
        ''' Attempt to load a module.  Throws an exception if unable to load module '''
        if self.module(module_name) != None:
            raise Exception(module_name + ' -- Module already loaded')
            return
        try:
            m = self.import_package(self.get_module_full_path(module_name))
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            #print(dir(e))
            #print(e.msg)
            #e.print_file_and_line()
            
            #print(repr(traceback.format_exception(exc_type, exc_value,
            #                              exc_traceback)))

            traceback.print_exception(exc_type, exc_value, exc_traceback)

            raise Exception(module_name + ' -- Module not loadable')
            return
        
        module = m.init(self)

    def add_loaded_module(self, name, mod):
        '''
        Append a loaded module to the dictionary of loaded modules
        Raises an exception if the module name alrady exists in the dictionary.
        '''
        if name in self.__loaded_modules:
            err_str = "Module " + name + " already loaded"
            raise Exception (err_str)
            return

        if not isinstance(mod, sc_module.SCModule):
            err_str = "Cannot add module " + name + " as a loaded module: it's not an SCModule"
            raise Exception (err_str)
            return

        self.__loaded_modules[name] = mod

    def clear_zipimport_cache(self):
        """Clear out cached entries from _zip_directory_cache.
        See http://www.digi.com/wiki/developer/index.php/Error_messages"""
        syspath_backup = list(sys.path)
        zipimport._zip_directory_cache.clear()
 
        # load back items onto sys.path
        sys.path = syspath_backup
       # add this too: see https://mail.python.org/pipermail/python-list/2005-May/353229.html
        sys.path_importer_cache.clear()
        # http://stackoverflow.com/questions/211100/pythons-import-doesnt-work-as-expected
        # has info on why this is necessary.

    def import_package(self, name):
        """Given a package name like 'foo.bar.quux', imports the package
        and returns the desired module.  Throws an exception if a package isn't found."""
        try:
            mod = __import__(name)
        except ImportError:
            self.clear_zipimport_cache()
            mod = __import__(name)
       
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
            
