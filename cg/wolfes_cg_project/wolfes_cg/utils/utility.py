#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, platform, enum
import pathlib
from wolfes_cg.utils import plogging

class HostSystem(enum.IntEnum):
    LINUX = 0
    WINDOWS = 1
    MACOS = 2
    END = 3

class ErrorCode(enum.IntEnum):
    SUCCESS = 0
    FAILURE = 1
    INVALID_VERSION = 2
    INVALID_ARGUMENT = 3
    NOT_SUPPORTED = 4
    FILE_NOT_FOUND = 5
    FILE_INVALID = 6
    END = 7

### make it cross platform
class UtilityFunctions(object):
    def __init__(self):
        self._logger = plogging.get_logger()
        self._hostsystem        = self.get_host_system()
        self._homedir:str       = self.get_host_homedir()
        self._tmpdir:str        = self.get_host_tmpdir()

    def get_host_system(self) -> HostSystem:
        str_host_sys = platform.system()
        if str_host_sys == "Linux":
            return HostSystem.LINUX
        elif str_host_sys == "Windows":
            return HostSystem.WINDOWS
        elif str_host_sys == "macOS":
            raise SystemError("MACOS not supported !".format(str_host_sys))
        else:
            raise SystemError("invalid host system [{}] !".format(str_host_sys))
    
    def get_host_homedir(self) -> str:
        return os.path.expanduser("~")
    
    def get_host_tmpdir(self) -> str:
        homedir = pathlib.Path(self._homedir)
        tmpdir = homedir.joinpath("tmp")
        return str(tmpdir)

    def make_file_path(self, parent_dir:str=None, file_name:str=None) -> str:
        if parent_dir:
            try:
                pdir = pathlib.Path(parent_dir)
                pdir.mkdir(parents=True, exist_ok=True)
                if file_name:
                    filedir = pdir.joinpath(file_name)
                    if filedir.exists():
                        self._logger.warning("file path {} already exists!".format(str(filedir)))
                    return str(filedir)
            except FileExistsError:
                self._logger.error("parent directory {} already exists!".format(parent_dir))
                return None
        else:
            return None