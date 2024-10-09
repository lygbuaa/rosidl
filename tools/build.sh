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

CMAKE_ARGS="--cmake-args -DBUILD_TESTING=OFF"

colcon build ${CMAKE_ARGS} --packages-up-to rosidl_adapter
colcon build ${CMAKE_ARGS} --packages-up-to rosidl_generator_c
colcon build ${CMAKE_ARGS} --packages-up-to rosidl_generator_cpp
colcon build ${CMAKE_ARGS} --packages-up-to rosidl_typesupport_introspection_c
colcon build ${CMAKE_ARGS} --packages-up-to rosidl_typesupport_introspection_cpp