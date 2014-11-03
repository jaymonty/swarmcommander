#!/bin/bash

#Super simple way of cleaning up.  Later we probably want to know exactly what
#PIDs to kill off.

USE_CONTAINERS=0

#parse options
while getopts ":C" opt; do
    case $opt in    
        C)
            USE_CONTAINERS=1
            ;;
    esac
done
shift $((OPTIND-1))

killall ArduPlane.elf
killall JSBSim
killall mavproxy.py
if [ $USE_CONTAINERS == 1 ]; then 
    sudo killall launch_payload.sh
    sudo killall roslaunch
else
    killall repeater.py
    killall roslaunch
    killall launch_payload.sh
fi

if [ $USE_CONTAINERS == 1 ]; then 
    sudo killall xterm
else
    killall xterm
fi
