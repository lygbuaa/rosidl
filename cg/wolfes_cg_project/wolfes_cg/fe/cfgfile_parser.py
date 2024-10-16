#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json, pathlib
from wolfes_cg.ir.wolfes_ir import *
from wolfes_cg.utils import plogging
from wolfes_cg.utils.utility import *

class BaseConfigParser(object):
    def __init__(self):
        self._logger = plogging.get_logger()
        self._cfgfile_path:pathlib.Path = None
        self._cfgfile_content:str = None

    ### check input file path if exists
    def check_input(self, cfgfile_path:str) -> ErrorCode:
        if len(cfgfile_path) < 4:
            self._logger.error("config file path [{}] invalid !".format(cfgfile_path))
            return ErrorCode.INVALID_ARGUMENT
        ### make it cross platform
        self._cfgfile_path = pathlib.Path(cfgfile_path)
        if cfgfile_path.find('~') != -1:
            self._cfgfile_path = self._cfgfile_path.expanduser()
            self._logger.warning("get posix file path with ~, expand to {}".format(str(self._cfgfile_path)))
        if not self._cfgfile_path.exists():
            self._logger.error("config file [{}] not found !".format(cfgfile_path))
            return ErrorCode.FILE_NOT_FOUND

        self._cfgfile_content = self._cfgfile_path.read_text()
        if len(self._cfgfile_content) < 2:
            self._logger.error("config file too short {} !".format(len(self._cfgfile_content)))
            return ErrorCode.FILE_INVALID

        return ErrorCode.SUCCESS

class JsonConfigParser(BaseConfigParser):
    def __init__(self):
        super(JsonConfigParser, self).__init__()
        self._logger.info("json version: {}".format(json.__version__))
        self._json_dict:str = None

    ### check input json format
    def check_input(self, cfgfile_path:str) -> ErrorCode:
        retcode = super(JsonConfigParser, self).check_input(cfgfile_path)
        if retcode != ErrorCode.SUCCESS:
            return retcode
        try:
            self._json_dict = json.loads(self._cfgfile_content)
        except ValueError as e:
            self._logger.error("json file invalid: {} !".format(e))
            return ErrorCode.FILE_INVALID

        self._logger.debug("json {}".format(self._json_dict))

        return ErrorCode.SUCCESS

if __name__ == '__main__':
    pass