#!/bin/bash

function find_ros2_ws_path() {
    # echo "@i@ --> find dir: ${0}"
    this_script_dir=$( dirname -- "$0"; )
    pwd_dir=$( pwd; )
    if [ "${this_script_dir:0:1}" = "/" ]
    then
        # echo "get absolute path ${this_script_dir}" > /dev/tty
        ros2_ws_path=${this_script_dir}"/../"
    else
        # echo "get relative path ${this_script_dir}" > /dev/tty
        ros2_ws_path=${pwd_dir}"/"${this_script_dir}"/../"
    fi
    echo "${ros2_ws_path}"
}

ROS2_WS_PATH=$( find_ros2_ws_path )
echo "ros2_ws_path: ${ROS2_WS_PATH}" 
cd ${ROS2_WS_PATH}

DEFAULT_MSG_FILE_PATH=${ROS2_WS_PATH}/test/example_msgs/msg/Example1.msg

# ros2 run rosidl_adapter msg2idl.py  ${DEFAULT_MSG_FILE_PATH}
python3 rosidl_adapter/scripts/msg2idl.py ${DEFAULT_MSG_FILE_PATH}