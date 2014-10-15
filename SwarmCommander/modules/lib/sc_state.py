"""
    Swarm Commander State class.  
    
    Holds global state information for the entire application.
    A reference to the State class is passed to modules.
"""

from SwarmCommander.modules.lib import sc_module

import sys, pip, zipfile, zipimport

class SCState(object):
    '''
    Contains state information intended to be passed between modules to give
    information about the state of the entire application.
    '''

    def __init__(self):
        self.__loaded_modules = {}
        self.__module_paths = []
        
    def module(self, name):
        ''' Find a module. Return none if no module of that name, or if module is private. '''
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
                if (next_module.rfind("/") != -1):
                    next_module = next_module[0:next_module.rfind("/")]
                file_list.append(next_module)

        return file_list        

    def load_module(self, module_name):
        ''' Attempt to load a module.  Throws an exception if unable to load module '''
        if self.module(module_name) != None:
            raise Exception('Module already loaded')
            return
        modpath = 'SwarmCommander.modules.sc_%s' % module_name
        try:
            m = self.import_package(modpath)
        except:
            raise Exception('Module not found')
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
            err_str = "Cannot module " + name + " as a loaded module: it's not an SCModule"
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
            
