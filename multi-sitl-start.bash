#!/bin/bash

usage()
{
cat <<EOF
Usage: $0 [options] num_SITLS [sitl_root_dir] [template_eeprom.bin]
Options:
    -C                      Start a linux container for each payload SITL
EOF
}

USE_CONTAINERS=0

#parse options
while getopts ":Ch" opt; do
    case $opt in    
        C)
            USE_CONTAINERS=1
            ;;
        h)
            usage
            exit 0
            ;;            
    esac
done
shift $((OPTIND-1))

if [ $# -lt 1 ]; then
    usage
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

#need the sudo passwd if using -C argument
if [ $USE_CONTAINERS == 1 ]; then 
    echo "Making Containers. "
    sudo echo "Ensuring we have sudo credentials available."
    multi-sitl-cleanup.bash -C
else
    multi-sitl-cleanup.bash
fi

#make sure ArduPlane build is up to date:
pushd $ACS_ROOT/ardupilot/ArduPlane || {
    echo "Failed to change to vehicle directory for ArduPlane, unable to update build."
}
    make sitl -j4 || {
        make clean
        make sitl -j4    
    }
popd

i=1
total_sitls=$1
while [ $i -le $total_sitls ]
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
    /usr/bin/xterm -hold -e "sim_vehicle.sh -N -I $i -v ArduPlane -L McMillan --aircraft testing --mission 0" &

    #Give each autopilot portion of SITL a chance to get started
    sleep 5

    cd $ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils

    if [ $USE_CONTAINERS == 1 ]; then 
        sudo -E /usr/bin/xterm -hold -e "$ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/launch_payload.sh -C -R $USER $i" &
    else
        /usr/bin/xterm -hold -e "$ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/launch_payload.sh $i" &
    fi  

    i=$(( $i + 1 ))
done

if [ $USE_CONTAINERS != 1 ]; then
   /usr/bin/xterm -hold -e "$ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/repeater.py -b 5555 $total_sitls & 
fi

