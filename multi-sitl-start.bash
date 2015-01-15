#!/bin/bash

USE_CONTAINERS=0
START_INDEX=1
NEED_BRIDGE=0

NET_DEVICE="eth0"

usage()
{
cat <<EOF
Usage: $0 [options] num_SITLS [sitl_root_dir] [template_eeprom.bin]
Options:
    -B         Set up and use SITL bridge (implies -D sitl_bridge)
    -C         Start a linux container for each payload SITL (implies -B)
    -D         Override default net device (default is eth0 -- don't use w/ -C)
    -I         Starting index for the group of SITLs
EOF
}

#parse options
while getopts ":I:BCD:h" opt; do
    case $opt in
        B)
            NET_DEVICE="sitl_bridge"
            ;;
        C)
            USE_CONTAINERS=1
            ;;
        D)
            NET_DEVICE=$OPTARG
            ;;
	    I)
            START_INDEX=$OPTARG
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

if [ $NET_DEVICE == "sitl_bridge" ]; then
    NEED_BRIDGE=1
fi

#need the sudo passwd if using -C argument
if [ $USE_CONTAINERS == 1 -o $NEED_BRIDGE == 1 ]; then 
    echo "Need sudo password."
    sudo echo "Ensuring we have sudo credentials available for cleanup and also later on in the script."
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

i=$START_INDEX
total_sitls=$(( $1 + $START_INDEX - 1 ))
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
        if [ $NEED_BRIDGE == 1 ]; then
            $ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/bridge_config.sh
        fi

        /usr/bin/xterm -hold -e "$ACS_ROOT/acs_ros_ws/src/autonomy-payload/utils/launch_payload.sh -D $NET_DEVICE $i" &
    fi  

    i=$(( $i + 1 ))
done

