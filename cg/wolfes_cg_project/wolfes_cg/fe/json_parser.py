#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from ir.wolfes_ir import *
from utils import plogging

def do_parse():
    global g_logger
    g_logger = plogging.get_logger()
    g_logger.info("json version: {}".format(json.__version__))

if __name__ == '__main__':
    do_parse()