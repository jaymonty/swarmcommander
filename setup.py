from setuptools import setup

import sys

version = "0.0.3"

#require python3
#exit with message if we're not using Python 3:
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

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
                'SwarmCommander.modules.sc_map',
                'SwarmCommander.modules.lib'],
      #note that we do not include all the real dependencies here (like matplotlib etc)
      # as that breaks the pip install. It seems that pip is not smart enough to
      # use the system versions of these dependencies, so it tries to download and install
      # large numbers of modules like numpy etc which may be already installed
      #
      #Also appears to not intall python 3 versions of what's in the list 
      #(at least on Ubuntu as of this writing)
      install_requires=['pyserial'],
      scripts=['swarm_commander.py']
      #TODO: package_data: see MAVProxy setup.py for an example
      #TODO: don't forget to add the commad at the end of the previous line :)
      #package_data={'SwarmCommander':
      #              'modules
      )
