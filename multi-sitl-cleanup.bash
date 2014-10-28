#!/bin/bash

#Super simple way of cleaning up.  Later we probably want to know exactly what
#PIDs to kill off.

killall ArduPlane.elf
killall JSBSim
killall mavproxy.py
sudo killall launch_payload_container.sh
killall roslaunch
killall xterm
sudo killall xterm
