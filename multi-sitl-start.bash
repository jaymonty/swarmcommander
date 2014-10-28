#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage $0 num_SITLs [sitl_root_dir] [template_eeprom.bin]"
    exit -45
fi

SITL_ROOT_DIR=$HOME/flying
if [ $# -ge 2 ]; then
    SITL_ROOT_DIR=$2
fi

template_eeprom_path=""
if [ $# -ge 3 ]; then
    template_eeprom_path=$3
fi

#need the sudo passwd
sudo echo "Ensuring we have sudo credentials available."

#TODO: later assume this script has been installed (remove "./")
./multi-sitl-cleanup.bash

i=1
while [ $i -le $1 ]
do
    echo "Starting SITL $i";

    #create sitl directory if it doesn't exist
    mkdir -p $SITL_ROOT_DIR/sitl$i

    #startup a new termianl and start the SITL
    cd $SITL_ROOT_DIR/sitl$i

    if [ -n "$template_eeprom_path" ]; then
        cp -f $template_eeprom_path .
    fi
    
    #run_in_terminal_window.sh "sim_vehicle.sh -I $i -v ArduPlane -L McMillan --aircraft testingDashboard --mission 0 --map --console"
    /usr/bin/xterm -hold -e "sim_vehicle.sh -N -I $i -v ArduPlane -L McMillan --aircraft testingDashboard --mission 0" &

    #Give each autopilot portion of SITL a chance to get started
    sleep 5

    cd $ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils

    sudo -E /usr/bin/xterm -hold -e "$ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/launch_payload_container.sh $i $USER" &

    i=$(( $i + 1 ))
done

