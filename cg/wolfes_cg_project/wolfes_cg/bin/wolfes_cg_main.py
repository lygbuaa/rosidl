#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, logging, pathlib
import argparse
this_project_path = str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath("../../"))
if not this_project_path in sys.path:
    sys.path.append(this_project_path)
from wolfes_cg.utils import plogging
from wolfes_cg.utils.utility import *
from wolfes_cg.fe.cfgfile_parser import JsonConfigParser
from wolfes_cg.ir.validate_ir import WOLfesIRValidator
from wolfes_cg._version import __version__

class WOLfesCG(object):
    def __init__(self):
        plogging.init_logger(level=logging.INFO, log_dir=self.get_logdir(), file_name="wolfes_cg")
        self._logger = plogging.get_logger()
        self.check_cmdargs()
        self._utility = UtilityFunctions()
        self._logger.debug("_hostsystem: {}, _homedir: {}, _tmpdir: {}".format(self._utility._hostsystem.name, self._utility._homedir, self._utility._tmpdir))
        self._logger.debug("cwd: {}, entry: {}".format(os.getcwd(), os.path.join(os.path.dirname(__file__), __file__)))
        self._json_parser = JsonConfigParser()
        self._ir_validator = WOLfesIRValidator()

    def get_logdir(self) -> str:
        homedir = pathlib.Path(os.path.expanduser("~"))
        tmpdir = homedir.joinpath("tmp")
        tmpdir.mkdir(parents=True, exist_ok=True)
        return str(tmpdir)

    def make_argparser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--version',        action="version",  version='***** %(prog)s {ver} *****'.format(ver=__version__))
        parser.add_argument('--loglevel',       nargs=1, type=int, default=[20],help='set log level, DEBUG=10, INFO=20, WARN=30, ERROR=40')
        parser.add_argument('-i', '--input',    nargs=1, type=str, help='input config file path, format *.json is supported')
        parser.add_argument('-o', '--output',   nargs=1, type=str, help='directory for generated files')
        return parser

    def check_cmdargs(self):
        self._argparser = self.make_argparser()
        try:
            self._args = self._argparser.parse_args(args=sys.argv[1:])
            self._logger.info("input args: {}".format(self._args))
        except Exception as e:
            self._argparser.print_help()
            self._logger.error("command line {} invalid".format(sys.argv[1:]))
            sys.exit(ErrorCode.INVALID_ARGUMENT)
        if not self._args.input:
            self._argparser.print_help()
            self._logger.error("command line {} missing --input".format(sys.argv[1:]))
            sys.exit(ErrorCode.INVALID_ARGUMENT)
        elif not self._args.output:
            self._argparser.print_help()
            self._logger.error("command line {} missing --output".format(sys.argv[1:]))
            sys.exit(ErrorCode.INVALID_ARGUMENT)
        if self._args.loglevel[0] in [int(logging.DEBUG), int(logging.INFO), int(logging.WARNING), int(logging.ERROR), int(logging.CRITICAL)]:
            self._logger.setLevel(self._args.loglevel[0])
            for handler in self._logger.handlers:
                handler.setLevel(self._args.loglevel[0])
            self._logger.warning("set loglevel: {}".format(self._args.loglevel[0]))
        else:
            self._logger.error("invalid loglevel: {}".format(self._args.loglevel[0]))
            sys.exit(ErrorCode.INVALID_ARGUMENT)

    def main(self) -> ErrorCode:
        ### check config file inputs
        if ".json" in self._args.input[0]:
            retcode = self._json_parser.check_input(self._args.input[0])
            if retcode != ErrorCode.SUCCESS:
                return retcode
        elif ".arxml" in self._args.input[0]:
            self._logger.error("arxml config file will support in future !")
            return ErrorCode.FAILURE
        else:
            self._logger.error("config file invalid {} type !".format(self._args.input[0]))
            return ErrorCode.FAILURE

        ### generate ir from config file
        obj_ir = self._json_parser.generate_ir()

        ### validate ir support
        if obj_ir and self._ir_validator.validate(obj_ir):
            self._logger.info("ir validation pass.")
        else:
            self._logger.error("ir validation failed !")
            return ErrorCode.FAILURE

        ### generate msgs

        ### generate codes

        ### generate cmake files

        return ErrorCode.SUCCESS

def main() -> int:
    wolfes_cg_obj = WOLfesCG()
    return wolfes_cg_obj.main()

if __name__ == '__main__':
    sys.exit(main() or 0)
