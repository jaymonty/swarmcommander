#!/usr/bin/env python3

from setuptools import setup

import sys, os

version = "0.0.7"

#require python3
#exit with message if we're not using Python 3:
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

#first generate all code from Qt .ui files as necessary
orig_dir = os.getcwd()
os.chdir("SwarmCommander/modules/sc_qt_gui")
os.system("make")
os.chdir(orig_dir)

setup(name='SwarmCommander',
      version=version,
      zip_safe=True,
      description='Swarm Commander Ground Control Station',
      long_description='A Ground Control Station (GCS) intended for use with swarms of up to 100 planes.  Developed by the Naval Postgraduate School as part of the Aerial Combat Swarms challenge.',
      url='coming soon',
      author='NPS ARSENL Lab',
      author_email='maday@nps.edu',
      classifiers=[
          'Devlopment Status :: 2 - Pre-Alpha',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: Science/Research',
          'License :: TBD',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scienctific/Engineering'],
      license='TBD',
      packages=['SwarmCommander',
                'SwarmCommander.modules',
                'SwarmCommander.modules.sc_acs_network',
                'SwarmCommander.modules.sc_map_tiler',
                'SwarmCommander.modules.sc_qt_gui',
                'SwarmCommander.modules.lib'],
      #note that we do not include all the real dependencies here (like matplotlib etc)
      # as that breaks the pip install. It seems that pip is not smart enough to
      # use the system versions of these dependencies, so it tries to download and install
      # large numbers of modules like numpy etc which may be already installed
      #
      #Also appears to not intall python 3 versions of what's in the list 
      #(at least on Ubuntu as of this writing)
      install_requires=['pyserial'],
      scripts=['swarm_commander.py',
               'SwarmCommander/tools/sc_map_prefetch.py',
               '../SiK/Firmware/tools/atcommander.py'],
      package_data={'SwarmCommander':
                    ['data/images/*.png']}
      )
