#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, struct, enum, platform
from typing import List

class WOLfesVersion:
    Major:int = 0
    Minor:int = 0
    Patch:int = 0
    Build:int = 0
    Res1:int = 0
    Res2:int = 0

class WOLfesPlatform(enum.IntEnum):
    LINUX = 0
    ANDROID = 1
    RTOS = 2
    QNX = 3
    RES1 = 4
    RES2 = 5
    END = 6

class WOLfesLang(enum.IntEnum):
    CPP = 0
    C = 1
    RUST = 2
    PYTHON = 3
    JAVA = 4
    RES1 = 5
    RES2 = 6
    END = 7

class WOLfesProtocolType(enum.IntEnum):
    INTRA = 0
    SEDDS = 1
    SOMEIP = 2
    ZMQ_IPC = 3
    ZMQ_TCP = 4
    ZMQ_EPGM = 5
    SHM = 6
    HYBRID = 7
    RES1 = 8
    RES2 = 9
    END = 10

class WOLfesMsgType(enum.IntEnum):
    PROTO = 0
    SOMEIP = 1
    FASTDDS = 2
    CYCLONEDDS = 3
    RTICONNEXT = 4
    ROS = 5
    RAW = 6
    CUSTOM = 7
    RES1 = 8
    RES2 = 9
    END = 10

class WOLfesTimerType(enum.IntEnum):
    STEADY = 0
    SYSTEM = 1
    CUSTOM = 2
    RES1 = 3
    RES2 = 4
    END = 5

### generated msg files are dict of WOLfesLang
class WOLfesCustomMsg(object):
    def __init__(self, type:WOLfesMsgType, src_file:str):
        self._type = type
        self._src_file = src_file
        self._header_files:dict = None
        self._src_files:dict = None

class WOLfesTimer:
    _id:str = "0"
    _type:WOLfesTimerType = WOLfesTimerType.END
    _period:int = 0
    _func_name:str = "" ### callback function

class WOLfesTopicPub:
    _id:str = "0"
    _topic_name:str = ""
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""
    _func_name:str = "" ### publish function

class WOLfesTopicSub:
    _id:str = "0"
    _topic_name:str = ""
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""
    _func_name:str = "" ### callback function

class WOLfesServiceServer:
    _id:str = "0"
    _service_name:str = ""
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""
    _func_name:str = "" ### server function

class WOLfesServiceClient:
    _id:str = "0"
    _service_name:str = ""
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""
    _func_name:str = "" ### client function

class WOLfesActionServer:
    _id:str = "0"
    _action_name:str = ""
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""
    _func_name:str = "" ### server function

class WOLfesActionClient:
    _id:str = "0"
    _action_name:str = ""
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""
    _func_name:str = "" ### client function

class WOLfesModuleType(enum.IntEnum):
    TIMER_PROC = 0
    SYNC_PROC = 1
    COND_PROC = 2
    RES1 = 3
    RES2 = 4
    END = 5

class WOLfesModuleIO:
    _id:str = "0"
    _msg_type:WOLfesMsgType = WOLfesMsgType.END
    _message:str = ""    ### optional
    _msg_src:str = ""

'''
# namespace for cpp-code, will embed into struct name for c-code.
'''
G_DEFAULT_NAMESPACE:str = "WOLfesApp"

'''
# class-name for cpp-code, will embed into struct-name for c-code.
'''
G_DEFAULT_CLASSNAME:str = "WOLfesNode"

class WOLfesIRNode(object):
    def __init__(self):
        self._classname:str                                 = G_DEFAULT_CLASSNAME
        self._qos_cfg:str                                   = ""
        self._timers:List[WOLfesTimer]                      = []
        self._topic_pubs:List[WOLfesTopicPub]               = []
        self._topic_subs:List[WOLfesTopicSub]               = []
        self._service_servers:List[WOLfesServiceServer]     = []
        self._service_clients:List[WOLfesServiceClient]     = []
        self._action_servers:List[WOLfesActionServer]       = []
        self._action_clients:List[WOLfesActionClient]       = []

class WOLfesIRModule(object):
    def __init__(self):
        self._type:WOLfesModuleType                         = WOLfesModuleType.END
        self._inputs:List[WOLfesModuleIO]                   = []
        self._outputs:List[WOLfesModuleIO]                  = []

class WOLfesIRApp(object):
    def __init__(self):
        self._namespace:str     = G_DEFAULT_NAMESPACE
        self._domain_id:int     = 0
        self._protocoltype:int  = WOLfesProtocolType.END
        self._scheduler_cfg:str = ""
        self._nodes:List[WOLfesIRNode]      = []
        self._modules:List[WOLfesIRModule]  = []
        self._identifiers:List[str]         = []

class WOLfesIR(object):
    def __init__(self):
        ### common fields
        self._platform:int          = WOLfesPlatform.END
        self._lang:int              = WOLfesLang.END
        self._version:WOLfesVersion = None
        ### apps
        self._apps:List[WOLfesIRApp] = []
        ## msg files
        self._custom_msgs:List[WOLfesCustomMsg] = []

if __name__ == '__main__':
    my_ir = WOLfesIR()
    print(my_ir._platform.name)

