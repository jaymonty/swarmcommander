#!/bin/bash

#TODO: allow specification of location of sitl directories

if [ $# -lt 1 ]; then
    echo "Usage $0 num_SITLs"
    exit -45
fi

#need the sudo passwd
sudo echo "Ensuring we have sudo credentials available."

#TODO: later assume this script has been installed (remove "./")
./multi-sitl-cleanup.bash

i=1
while [ $i -le $1 ]
do

    echo "Starting SITL $i";

    #TODO: create sitl directory if it doesn't exist

    #startup a new termianl and start the SITL
    cd /home/maday/flying/sitl$i
    
    #run_in_terminal_window.sh "sim_vehicle.sh -I $i -v ArduPlane -L McMillan --aircraft testingDashboard --mission 0 --map --console"
    /usr/bin/xterm -hold -e "sim_vehicle.sh -N -I $i -v ArduPlane -L McMillan --aircraft testingDashboard --mission 0" &

    #Give each autopilot portion of SITL a chance to get started
    sleep 2

    cd $ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils

    sudo -E /usr/bin/xterm -hold -e "$ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/launch_payload_container.sh $i $USER" &

    i=$(( $i + 1 ))
done

