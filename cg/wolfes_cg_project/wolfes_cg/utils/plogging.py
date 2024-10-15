#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, sys
from os import path

G_PLOGGING_NAME = "g_plogger_name"
'''
    logging.DEBUG,     #debug_mode
    logging.INFO,       #0
    logging.WARNING,    #1
    logging.ERROR,      #2
    logging.CRITICAL]   #3
'''
G_PLOGGING_LEVEL = logging.DEBUG #logging.INFO

# first, call init_logger() in the main.py file
def init_logger(level=logging.DEBUG, log_dir="./", file_name=None) -> logging.Logger:
    global G_PLOGGING_NAME, G_PLOGGING_LEVEL

    G_PLOGGING_LEVEL = level
    logger = logging.getLogger(G_PLOGGING_NAME)
    logger.setLevel(G_PLOGGING_LEVEL)

    # Set console logging
    console_handler = logging.StreamHandler()
    ### show filename instead of pathname
    console_formatter = logging.Formatter(fmt="%(levelname).1s%(asctime)s.%(msecs)03d    %(process)d %(filename)s:%(lineno)d] %(message)s", datefmt="%H:%M:%S")
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(G_PLOGGING_LEVEL)
    logger.addHandler(console_handler)

    if log_dir and file_name:
        # Setup file logging
        file_handler = logging.FileHandler(path.join(log_dir, file_name + ".log"), mode="w")
        ### log pathname instead of filename
        file_formatter = logging.Formatter(fmt="%(levelname).1s%(asctime)s.%(msecs)03d    %(process)d %(pathname)s:%(lineno)d] %(message)s", datefmt="%y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(G_PLOGGING_LEVEL)
        logger.addHandler(file_handler)

    return logger

# then, call get_logger() in every other *.py files
# now, every *.py file will print into the same log file
def get_logger() -> logging.Logger:
    global G_PLOGGING_NAME
    return logging.getLogger(G_PLOGGING_NAME)

if __name__ == '__main__':
    # create logger
    init_logger(level=logging.INFO, log_dir="./", file_name="plogging_test", )
    logger = get_logger()
    # use logger
    logger.debug("plogging debug")
    logger.info("plogging info")
    logger.warning("plogging warning")
    logger.error("plogging error")
    logger.critical("plogging critical")

    sys.exit(0)