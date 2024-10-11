#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
### version: 0.0.1
### date: 2024-10-10
'''

import os, sys, struct, enum
from typing import List

G_IR_VERSION:str = "0.0.1"

class WOLfesAPI(enum.IntEnum):
    NODE = 0
    MODULE = 1
    RES1 = 2
    RES2 = 3
    END = 4

class WOLfesPlatform(enum.IntEnum):
    LINUX = 0
    QNX = 1
    RTOS = 2
    RES1 = 3
    RES2 = 4
    END = 5

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

class WOLfesVersion:
    Major:int = 0
    Minor:int = 0
    Patch:int = 0
    Build:int = 0
    Res1:int = 0
    Res2:int = 0

class WOLfesConfigFiles:
    Qos:str = ""
    Scheduler:str = ""
    Res1:str = ""
    Res2:str = ""

class WOLfesTopicPub:
    Id:str = "0"
    TopicName:str = ""
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""
    PfName:str = "" ### publish function

class WOLfesTopicSub:
    Id:str = "0"
    TopicName:str = ""
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""
    CbName:str = "" ### callback function

class WOLfesServiceServer:
    Id:str = "0"
    ServiceName:str = ""
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""
    SfName:str = "" ### server function

class WOLfesServiceClient:
    Id:str = "0"
    ServiceName:str = ""
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""
    CfName:str = "" ### client function

class WOLfesActionServer:
    Id:str = "0"
    ActionName:str = ""
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""
    SfName:str = "" ### server function

class WOLfesActionClient:
    Id:str = "0"
    ActionName:str = ""
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""
    CfName:str = "" ### client function

class WOLfesTimer:
    Id:str = "0"
    Type:WOLfesTimerType = WOLfesTimerType.END
    Period:int = 0
    CbName:str = "" ### callback function

class WOLfesModuleType(enum.IntEnum):
    TIMER_PROC = 0
    SYNC_PROC = 1
    COND_PROC = 2
    RES1 = 3
    RES2 = 4
    END = 5

class WOLfesModuleIO:
    Id:str = "0"
    MsgType:WOLfesMsgType = WOLfesMsgType.END
    MsgName:str = ""    ### optional
    MsgSrc:str = ""

'''
# namespace for cpp-code, will embed into struct name for c-code.
'''
G_DEFAULT_NAMESPACE:str = "WOLfesSpace"

'''
# class-name for cpp-code, will embed into struct-name for c-code.
'''
G_DEFAULT_CLASSNAME:str = "WOLfesApp"

class WOLfesBaseIR(object):
    def __init__(self):
        self._api:int           = WOLfesAPI.END
        self._platform:int      = WOLfesPlatform.END
        self._lang:int          = WOLfesLang.END
        self._version           = WOLfesVersion
        self._cfg_files         = WOLfesConfigFiles
        self._namespace:str     = G_DEFAULT_NAMESPACE
        self._classname:str     = G_DEFAULT_CLASSNAME
        self._protocoltype:int  = WOLfesProtocolType.END

class WOLfesNodeIR(WOLfesBaseIR):
    def __init__(self):
        super(WOLfesNodeIR, self).__init__()
        self._topic_pubs:List[WOLfesTopicPub]               = []
        self._topic_subs:List[WOLfesTopicSub]               = []
        self._service_servers:List[WOLfesServiceServer]     = []
        self._service_clients:List[WOLfesServiceClient]     = []
        self._action_servers:List[WOLfesActionServer]       = []
        self._action_clients:List[WOLfesActionClient]       = []
        self._timers:List[WOLfesTimer]                      = []

class WOLfesModuleIR(WOLfesBaseIR):
    def __init__(self):
        super(WOLfesModuleIR, self).__init__()
        self._type:WOLfesModuleType                         = WOLfesModuleType.END
        self._inputs:List[WOLfesModuleIO]                   = []
        self._outputs:List[WOLfesModuleIO]                  = []

if __name__ == '__main__':
    my_node_ir = WOLfesNodeIR()
    my_module_ir = WOLfesModuleIR()
    print(my_node_ir._namespace)
    print(my_module_ir._classname)


