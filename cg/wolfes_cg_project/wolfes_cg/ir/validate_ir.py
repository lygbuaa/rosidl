import os, sys, re, pathlib
from typing import List
this_project_path = str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath("../../"))
if not this_project_path in sys.path:
    sys.path.append(this_project_path)
from wolfes_cg.utils import plogging
from wolfes_cg.utils.utility import *
from wolfes_cg.ir.wolfes_ir import *

G_SUPPORTED_WOLFES_VERSION = [
    "0.7.0",
    "0.8.0",
    "0.9.0",
    "1.0.0"
]

class WOLfesIRValidator(object):
    def __init__(self):
        self._logger = plogging.get_logger()
        self._norm_support_version_list = self.read_wolfes_version_list()

    def validate(self, ir:WOLfesIR) -> bool:
        if ir is None:
            self._logger.error("ir object is None !")
            return False
        ### [step-0] check version
        if not self.validate_wolfes_version(ir._version):
            return False

        ### check platform support according to version
        ### check language support according to version
        for i in range(0, len(ir._apps)):
            _app = ir._apps[i]
            ### check protocol type and domain_id
            for j in range(0, len(_app._nodes)):
                _node = _app._nodes[j]
                ### find out custom msgs, and check type and existence
                ir._custom_msgs = None

            ### TODO: modules will be support in future

        return True

    def parse_version_string(self, ver_str:str, re_search=re.compile(r'[^0-9.]').search) -> WOLfesVersion:
        ### first check if version string if valid, only with 0-9 and .
        if len(ver_str) < 1 or bool(re_search(ver_str)):
            self._logger.error("version string \"{}\" invalid !".format(ver_str))
            raise ValueError("version string \"{}\" invalid !".format(ver_str))
        numbers = ver_str.split(".")
        ver_obj = WOLfesVersion()
        if len(numbers) >= 1:
            ver_obj.Major = int(numbers[0])
        if len(numbers) >= 2:
            ver_obj.Minor = int(numbers[1])
        if len(numbers) >= 3:
            ver_obj.Patch = int(numbers[2])
        if len(numbers) == 4:
            ver_obj.Build = int(numbers[3])
        self._logger.debug("version numbers: [{:3d}.{:3d}.{:3d}.{:3d}]".format(ver_obj.Major, ver_obj.Minor, ver_obj.Patch, ver_obj.Build))
        if len(numbers) > 4:
            self._logger.warning("version numbers after [{:3d}.{:3d}.{:3d}.{:3d}] are discard !".format(ver_obj.Major, ver_obj.Minor, ver_obj.Patch, ver_obj.Build))
        return ver_obj

    ### normalize version string into {:08s}.{:08s}.{:08s} style for comparing convenience
    def read_wolfes_version_list(self) -> List[str]:
        norm_list = []
        for ver_str in G_SUPPORTED_WOLFES_VERSION:
            ver_obj = self.parse_version_string(ver_str)
            ### TODO: only Major and Minor version is considered.
            norm_str = "{:08s}.{:08s}".format(str(ver_obj.Major), str(ver_obj.Minor))
            norm_list.append(norm_str)
        self._logger.error("normalized version list: {}".format(norm_list))
        return norm_list

    def validate_wolfes_version(self, ver_obj:WOLfesVersion) -> bool:
        if ver_obj is None:
            self._logger.error("ver_obj is None !")
            return False
        ### normalize version into string
        norm_str = "{:08s}.{:08s}".format(str(ver_obj.Major), str(ver_obj.Minor))
        if (norm_str in self._norm_support_version_list):
            self._logger.debug("version {:s}.{:s} validated.".format(str(ver_obj.Major), str(ver_obj.Minor)))
            return True
        else:
            self._logger.error("version {:s}.{:s} not in the support list {} !".format(str(ver_obj.Major), str(ver_obj.Minor), G_SUPPORTED_WOLFES_VERSION))
            return False

if __name__ == '__main__':
    validator = WOLfesIRValidator()