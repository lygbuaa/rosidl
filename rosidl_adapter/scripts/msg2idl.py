#!/usr/bin/env python3

# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

### using local scripts, not system scripts in /opt/ros/foxy/lib/python3.8/site-packages
### do remove rosidl packages in /opt/ros/foxy/lib/python3.8/site-packages
import sys, logging
sys.path.append('/home/hugoliu/github/colcon_ws/rosidl')
sys.path.append('/home/hugoliu/github/colcon_ws/rosidl/rosidl_adapter')
print(sys.path)
from rosidl_adapter.cli import convert_files_to_idl
from rosidl_adapter.msg import convert_msg_to_idl
from utils import plogging

if __name__ == '__main__':
    global g_logger
    plogging.init_logger(log_dir="./", file_name="msg2idl", level=logging.INFO)
    g_logger = plogging.get_logger()
    g_logger.info("init g_logger in {}".format(__file__))

    convert_files_to_idl('.msg', convert_msg_to_idl)
