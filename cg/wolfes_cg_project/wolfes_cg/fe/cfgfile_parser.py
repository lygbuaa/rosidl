#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json, pathlib, re, sys, os
from typing import Any
this_project_path = str(pathlib.Path(os.path.dirname(os.path.abspath(__file__))).joinpath("../../"))
if not this_project_path in sys.path:
    sys.path.append(this_project_path)
from wolfes_cg.ir.wolfes_ir import *
from wolfes_cg.utils import plogging
from wolfes_cg.utils.utility import *

class BaseConfigParser(object):
    def __init__(self):
        self._logger = plogging.get_logger()
        self._utils = UtilityFunctions()
        self._cfgfile_path:pathlib.Path = None
        self._cfgfile_content:str = None
        self._ir:WOLfesIR         = None

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
    
    ### check config inputs and transfer into IR
    def generate_ir(self) -> ErrorCode:
        self._ir = None
        self._logger.error("stub !")
        return ErrorCode.FAILURE
    
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
        self._logger.info("wolfes_version: [{:d}.{:d}.{:d}.{:d}]".format(ver_obj.Major, ver_obj.Minor, ver_obj.Patch, ver_obj.Build))
        if len(numbers) > 4:
            self._logger.warning("version numbers after [{:d}.{:d}.{:d}.{:d}] are discard !".format(ver_obj.Major, ver_obj.Minor, ver_obj.Patch, ver_obj.Build))
        return ver_obj

### support single comment line in *.json file, comment line start with '//'
class JsonDecoderWithComments(json.JSONDecoder):
    def __init__(self, **kw):
        super().__init__(**kw)

    def decode(self, s: str) -> Any:
        s = '\n'.join(l for l in s.split('\n') if not l.lstrip(' ').startswith('//'))
        return super().decode(s)

class JsonConfigParser(BaseConfigParser):
    def __init__(self):
        super(JsonConfigParser, self).__init__()
        self._logger.info("json version: {}".format(json.__version__))
        self._json_obj:str = None

    ### check input json format
    def check_input(self, cfgfile_path:str) -> ErrorCode:
        retcode = super(JsonConfigParser, self).check_input(cfgfile_path)
        if retcode != ErrorCode.SUCCESS:
            return retcode
        try:
            self._json_obj = json.loads(self._cfgfile_content, cls=JsonDecoderWithComments)
        except ValueError as e:
            self._logger.error("json file invalid: {} !".format(e))
            return ErrorCode.FILE_INVALID

        self._logger.debug("_json_obj:\n{}".format(json.dumps(self._json_obj, indent=2)))

        return ErrorCode.SUCCESS

    def generate_ir(self) -> WOLfesIR:
        self._ir = WOLfesIR()
        ### common fields
        if "wolfes_version" in self._json_obj:
            self._ir._version = super(JsonConfigParser, self).parse_version_string(self._json_obj["wolfes_version"])
        else:
            self._logger.error("\"wolfes_version\" is required but missing !")
            raise KeyError("\"wolfes_version\" is required but missing !")

        if "platform" in self._json_obj:
            self._ir._platform = WOLfesPlatform(int(self._json_obj["platform"]))
            self._logger.debug("_platform: {}".format(self._ir._platform.name))
        else:
            self._logger.error("\"platform\" is required but missing !")
            raise KeyError("\"platform\" is required but missing !")

        if "lang" in self._json_obj:
            self._ir._lang = WOLfesLang(int(self._json_obj["lang"]))
            self._logger.debug("_lang: {}".format(self._ir._lang.name))
        else:
            self._logger.error("\"lang\" is required but missing !")
            raise KeyError("\"lang\" is required but missing !")

        ### apps
        for i in range(0, len(self._json_obj["apps"])):
            app_obj_i = self._json_obj["apps"][i]
            _app = WOLfesIRApp()
            if "namespace" in app_obj_i and type(app_obj_i["namespace"]) is str:
                _app._namespace = str(app_obj_i["namespace"])
                if not self._utils.check_identifier(_app._namespace):
                    self._logger.error("app[{}] namespace {} is invalid identifier !".format(i, _app._namespace))
                    raise KeyError("app[{}] namespace {} is invalid identifier !".format(i, _app._namespace))
            else:
                self._logger.error("app[{}] \"namespace\" is required but missing !".format(i))
                raise KeyError("app[{}] \"namespace\" is required but missing !".format(i))

            if "domain_id" in app_obj_i:
                _app._domain_id = int(app_obj_i["domain_id"])
            else:
                self._logger.warning("app[{}] \"domain_id\" is optional and missing !".format(i))

            if "protocol_type" in app_obj_i:
                _app._protocoltype = WOLfesProtocolType(int(app_obj_i["protocol_type"]))
            else:
                self._logger.error("app[{}] \"protocol_type\" is required but missing !".format(i))
                raise KeyError("app[{}] \"protocol_type\" is required but missing !".format(i))

            if "scheduler_config" in app_obj_i and type(app_obj_i["scheduler_config"]) is str:
                _app._scheduler_cfg = str(app_obj_i["scheduler_config"])
                ### check scheduler_config exists
                if not pathlib.Path(_app._scheduler_cfg).exists():
                    self._logger.warning("app[{}] scheduler config file \"{}\" not exists !".format(i, _app._scheduler_cfg))
                    raise FileExistsError("app[{}] scheduler config file \"{}\" not exists !".format(i, _app._scheduler_cfg))
            else:
                self._logger.warning("app[{}] \"scheduler_config\" is optional and missing !".format(i))

            ### nodes
            for j in range(0, len(app_obj_i["nodes"])):
                node_obj_j = app_obj_i["nodes"][j]
                _node = WOLfesIRNode()
                if "classname" in node_obj_j and type(node_obj_j["classname"]) is str:
                    _node._classname = str(node_obj_j["classname"])
                    if not self._utils.check_identifier(_node._classname):
                        self._logger.error("app[{}]-node[{}] classname {} is invalid identifier!".format(i, j, _node._classname))
                        raise KeyError("app[{}]-node[{}] classname {} is invalid identifier!".format(i, j, _node._classname))
                    _app._identifiers.append(_node._classname)
                else:
                    self._logger.error("app[{}]-node[{}] \"classname\" is required but missing !".format(i, j))
                    raise KeyError("app[{}]-node[{}] \"classname\" is required but missing !".format(i, j))
                if "qos_config" in app_obj_i and type(node_obj_j["qos_config"]) is str:
                    _node._qos_cfg = str(node_obj_j["qos_config"])
                    ### check qos_config exists
                    if not pathlib.Path(_node._qos_cfg).exists():
                        self._logger.warning("app[{}]-node[{}] qos config file \"{}\" not exists !".format(i, j, _node._qos_cfg))
                        raise FileExistsError("app[{}]-node[{}] qos config file \"{}\" not exists !".format(i, j, _node._qos_cfg))
                else:
                    self._logger.warning("app[{}]-node[{}] \"qos_config\" is optional and missing !".format(i, j))

                ### timers
                for k in range(0, len(node_obj_j["timers"])):
                    timer_obj_k = node_obj_j["timers"][k]
                    _timer = WOLfesTimer()
                    if "identifier" in timer_obj_k and type(timer_obj_k["identifier"]) is str:
                        _timer._id = str(timer_obj_k["identifier"])
                        if not self._utils.check_identifier(_timer._id):
                            self._logger.error("app[{}]-node[{}]-timer[{}] identifier {} is invalid identifier!".format(i, j, _timer._id))
                            raise KeyError("app[{}]-node[{}]-timer[{}] identifier {} is invalid identifier!".format(i, j, _timer._id))
                    else:
                        ### make default identifier.
                        _timer._id = "_timer_{:s}".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-timer[{}] \"id\" is optional and missing, using default {} !".format(i, j, k, _timer._id))
                    _app._identifiers.append(_timer._id)

                    if "type" in timer_obj_k:
                        _timer._type = str(timer_obj_k["type"])
                    else:
                        self._logger.error("app[{}]-node[{}]-timer[{}] \"type\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-timer[{}] \"type\" is required but missing !".format(i, j, k))

                    if "period" in timer_obj_k:
                        _timer._period = int(timer_obj_k["period"])
                    else:
                        self._logger.error("app[{}]-node[{}]-timer[{}] \"period\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-timer[{}] \"period\" is required but missing !".format(i, j, k))

                    if "cb_function" in timer_obj_k and type(timer_obj_k["cb_function"]) is str:
                        _timer._func_name = str(timer_obj_k["cb_function"])
                        if not self._utils.check_identifier(_timer._func_name):
                            self._logger.error("app[{}]-node[{}]-timer[{}] cb_function {} is invalid identifier!".format(i, j, k, _timer._func_name))
                            raise KeyError("app[{}]-node[{}]-timer[{}] cb_function {} is invalid identifier!".format(i, j, k, _timer._func_name))
                    else:
                        _timer._func_name = "__Timer{:s}Cb".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-timer[{}] \"cb_function\" is optional and missing, using default {} !".format(i, j, k, _timer._func_name))
                    _app._identifiers.append(_timer._func_name)

                    _node._timers.append(_timer)

                ### topic_pubs
                for k in range(0, len(node_obj_j["topic_pubs"])):
                    topic_pub_obj_k = node_obj_j["topic_pubs"][k]
                    _topic_pub = WOLfesTopicPub()
                    if "identifier" in topic_pub_obj_k and type(topic_pub_obj_k["identifier"]) is str:
                        _topic_pub._id = str(topic_pub_obj_k["identifier"])
                        if not self._utils.check_identifier(_topic_pub._id):
                            self._logger.error("app[{}]-node[{}]-topic_pub[{}] identifier {} is invalid identifier!".format(i, j, _topic_pub._id))
                            raise KeyError("app[{}]-node[{}]-topic_pub[{}] identifier {} is invalid identifier!".format(i, j, _topic_pub._id))
                    else:
                        _topic_pub._id = "_topic_pub_{:s}".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-topic_pub[{}] \"identifier\" is optional and missing, using default {} !".format(i, j, k, _topic_pub._id))
                    _app._identifiers.append(_topic_pub._id)

                    if "topic_name" in topic_pub_obj_k:
                        _topic_pub._topic_name = str(topic_pub_obj_k["topic_name"])
                    else:
                        self._logger.error("app[{}]-node[{}]-topic_pub[{}] \"topic_name\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-topic_pub[{}] \"topic_name\" is required but missing !".format(i, j, k))

                    if "message" in topic_pub_obj_k:
                        _topic_pub._message = str(topic_pub_obj_k["message"])
                    else:
                        self._logger.error("app[{}]-node[{}]-topic_pub[{}] \"message\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-topic_pub[{}] \"message\" is required but missing !".format(i, j, k))

                    if "msg_type" in topic_pub_obj_k:
                        _topic_pub._msg_type = str(topic_pub_obj_k["msg_type"])
                    else:
                        self._logger.error("app[{}]-node[{}]-topic_pub[{}] \"msg_type\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-topic_pub[{}] \"msg_type\" is required but missing !".format(i, j, k))

                    if "msg_src" in topic_pub_obj_k:
                        _topic_pub._msg_src = str(topic_pub_obj_k["msg_src"])
                        ### check file exists() only if custom-defined
                    else:
                        self._logger.warning("app[{}]-node[{}]-topic_pub[{}] \"msg_src\" is optional and missing !".format(i, j, k))

                    if "pub_function" in topic_pub_obj_k and type(topic_pub_obj_k["pub_function"]) is str:
                        _topic_pub._func_name = str(topic_pub_obj_k["pub_function"])
                        if not self._utils.check_identifier(_topic_pub._func_name):
                            self._logger.error("app[{}]-node[{}]-topic_pub[{}] pub_function {} is invalid identifier!".format(i, j, k, _topic_pub._func_name))
                            raise KeyError("app[{}]-node[{}]-topic_pub[{}] pub_function {} is invalid identifier!".format(i, j, k, _topic_pub._func_name))
                    else:
                        _topic_pub._func_name = "__TopicPub{:s}Pub".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-topic_pub[{}] \"pub_function\" is optional and missing, using default {} !".format(i, j, k, _topic_pub._func_name))
                    _app._identifiers.append(_topic_pub._func_name)
                    _node._topic_pubs.append(_topic_pub)

                ### topic_subs
                for k in range(0, len(node_obj_j["topic_subs"])):
                    topic_sub_obj_k = node_obj_j["topic_subs"][k]
                    _topic_sub = WOLfesTopicSub()
                    if "identifier" in topic_sub_obj_k and type(topic_sub_obj_k["identifier"]) is str:
                        _topic_sub._id = str(topic_sub_obj_k["identifier"])
                        if not self._utils.check_identifier(_topic_sub._id):
                            self._logger.error("app[{}]-node[{}]-topic_sub[{}] identifier {} is invalid identifier!".format(i, j, _topic_sub._id))
                            raise KeyError("app[{}]-node[{}]-topic_sub[{}] identifier {} is invalid identifier!".format(i, j, _topic_sub._id))
                    else:
                        _topic_sub._id = "_topic_sub_{:s}".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-topic_sub[{}] \"identifier\" is optional and missing, using default {} !".format(i, j, k, _topic_sub._id))
                    _app._identifiers.append(_topic_sub._id)

                    if "topic_name" in topic_sub_obj_k:
                        _topic_sub._topic_name = str(topic_sub_obj_k["topic_name"])
                    else:
                        self._logger.error("app[{}]-node[{}]-topic_sub[{}] \"topic_name\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-topic_sub[{}] \"topic_name\" is required but missing !".format(i, j, k))

                    if "message" in topic_sub_obj_k:
                        _topic_sub._message = str(topic_sub_obj_k["message"])
                    else:
                        self._logger.error("app[{}]-node[{}]-topic_sub[{}] \"message\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-topic_sub[{}] \"message\" is required but missing !".format(i, j, k))

                    if "msg_type" in topic_sub_obj_k:
                        _topic_sub._msg_type = str(topic_sub_obj_k["msg_type"])
                    else:
                        self._logger.error("app[{}]-node[{}]-topic_sub[{}] \"msg_type\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-topic_sub[{}] \"msg_type\" is required but missing !".format(i, j, k))

                    if "msg_src" in topic_sub_obj_k:
                        _topic_sub._msg_src = str(topic_sub_obj_k["msg_src"])
                        ### check file exists() only if custom-defined
                    else:
                        self._logger.warning("app[{}]-node[{}]-topic_sub[{}] \"msg_src\" is optional and missing !".format(i, j, k))

                    if "cb_function" in topic_sub_obj_k and type(topic_sub_obj_k["cb_function"]) is str:
                        _topic_sub._func_name = str(topic_sub_obj_k["cb_function"])
                        if not self._utils.check_identifier(_topic_sub._func_name):
                            self._logger.error("app[{}]-node[{}]-topic_sub[{}] cb_function {} is invalid identifier!".format(i, j, k, _topic_sub._func_name))
                            raise KeyError("app[{}]-node[{}]-topic_sub[{}] cb_function {} is invalid identifier!".format(i, j, k, _topic_sub._func_name))
                    else:
                        _topic_sub._func_name = "__TopicSub{:s}Cb".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-topic_sub[{}] \"cb_function\" is optional and missing, using default {} !".format(i, j, k, _topic_sub._func_name))
                    _app._identifiers.append(_topic_sub._func_name)
                    _node._topic_subs.append(_topic_sub)

                ### service_servers
                for k in range(0, len(node_obj_j["service_servers"])):
                    service_server_obj_k = node_obj_j["service_servers"][k]
                    _service_server = WOLfesServiceServer()
                    if "identifier" in service_server_obj_k and type(service_server_obj_k["identifier"]) is str:
                        _service_server._id = str(service_server_obj_k["identifier"])
                        if not self._utils.check_identifier(_service_server._id):
                            self._logger.error("app[{}]-node[{}]-service_server[{}] identifier {} is invalid identifier!".format(i, j, _service_server._id))
                            raise KeyError("app[{}]-node[{}]-service_server[{}] identifier {} is invalid identifier!".format(i, j, _service_server._id))
                    else:
                        _service_server._id = "_service_server_{:s}".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-service_server[{}] \"identifier\" is optional and missing, using default {} !".format(i, j, k, _service_server._id))
                    _app._identifiers.append(_service_server._id)

                    if "service_name" in service_server_obj_k:
                        _service_server._service_name = str(service_server_obj_k["service_name"])
                    else:
                        self._logger.error("app[{}]-node[{}]-service_server[{}] \"service_name\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-service_server[{}] \"service_name\" is required but missing !".format(i, j, k))

                    if "message" in service_server_obj_k:
                        _service_server._message = str(service_server_obj_k["message"])
                    else:
                        self._logger.error("app[{}]-node[{}]-service_server[{}] \"message\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-service_server[{}] \"message\" is required but missing !".format(i, j, k))

                    if "msg_type" in service_server_obj_k:
                        _service_server._msg_type = str(service_server_obj_k["msg_type"])
                    else:
                        self._logger.error("app[{}]-node[{}]-service_server[{}] \"msg_type\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-service_server[{}] \"msg_type\" is required but missing !".format(i, j, k))

                    if "msg_src" in service_server_obj_k:
                        _service_server._msg_src = str(service_server_obj_k["msg_src"])
                        ### check file exists() only if custom-defined
                    else:
                        self._logger.warning("app[{}]-node[{}]-service_server[{}] \"msg_src\" is optional and missing !".format(i, j, k))

                    if "res_function" in service_server_obj_k and type(service_server_obj_k["res_function"]) is str:
                        _service_server._func_name = str(service_server_obj_k["res_function"])
                        if not self._utils.check_identifier(_service_server._func_name):
                            self._logger.error("app[{}]-node[{}]-service_server[{}] res_function {} is invalid identifier!".format(i, j, k, _service_server._func_name))
                            raise KeyError("app[{}]-node[{}]-service_server[{}] res_function {} is invalid identifier!".format(i, j, k, _service_server._func_name))
                    else:
                        _service_server._func_name = "__ServiceServer{:s}Res".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-service_server[{}] \"res_function\" is optional and missing, using default {} !".format(i, j, k, _service_server._func_name))
                    _app._identifiers.append(_service_server._func_name)
                    _node._service_servers.append(_service_server)

                ### service_clients
                for k in range(0, len(node_obj_j["service_clients"])):
                    service_client_obj_k = node_obj_j["service_clients"][k]
                    _service_client = WOLfesServiceClient()
                    if "identifier" in service_client_obj_k and type(service_client_obj_k["identifier"]) is str:
                        _service_client._id = str(service_client_obj_k["identifier"])
                        if not self._utils.check_identifier(_service_client._id):
                            self._logger.error("app[{}]-node[{}]-service_client[{}] identifier {} is invalid identifier!".format(i, j, _service_client._id))
                            raise KeyError("app[{}]-node[{}]-service_client[{}] identifier {} is invalid identifier!".format(i, j, _service_client._id))
                    else:
                        _service_client._id = "_service_client_{:s}".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-service_client[{}] \"identifier\" is optional and missing, using default {} !".format(i, j, k, _service_client._id))
                    _app._identifiers.append(_service_client._id)

                    if "service_name" in service_client_obj_k:
                        _service_client._service_name = str(service_client_obj_k["service_name"])
                    else:
                        self._logger.error("app[{}]-node[{}]-service_client[{}] \"service_name\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-service_client[{}] \"service_name\" is required but missing !".format(i, j, k))

                    if "message" in service_client_obj_k:
                        _service_client._message = str(service_client_obj_k["message"])
                    else:
                        self._logger.error("app[{}]-node[{}]-service_client[{}] \"message\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-service_client[{}] \"message\" is required but missing !".format(i, j, k))

                    if "msg_type" in service_client_obj_k:
                        _service_client._msg_type = str(service_client_obj_k["msg_type"])
                    else:
                        self._logger.error("app[{}]-node[{}]-service_client[{}] \"msg_type\" is required but missing !".format(i, j, k))
                        raise KeyError("app[{}]-node[{}]-service_client[{}] \"msg_type\" is required but missing !".format(i, j, k))

                    if "msg_src" in service_client_obj_k:
                        _service_client._msg_src = str(service_client_obj_k["msg_src"])
                        ### check file exists() only if custom-defined
                    else:
                        self._logger.warning("app[{}]-node[{}]-service_client[{}] \"msg_src\" is optional and missing !".format(i, j, k))

                    if "req_function" in service_client_obj_k and type(service_client_obj_k["req_function"]) is str:
                        _service_client._func_name = str(service_client_obj_k["req_function"])
                        if not self._utils.check_identifier(_service_client._func_name):
                            self._logger.error("app[{}]-node[{}]-service_server[{}] req_function {} is invalid identifier!".format(i, j, k, _service_client._func_name))
                            raise KeyError("app[{}]-node[{}]-service_server[{}] req_function {} is invalid identifier!".format(i, j, k, _service_client._func_name))
                    else:
                        _service_client._func_name = "__ServiceClient{:s}Req".format(str(k))
                        self._logger.warning("app[{}]-node[{}]-service_client[{}] \"req_function\" is optional and missing, using default {} !".format(i, j, k, _service_client._func_name))
                    _app._identifiers.append(_service_client._func_name)
                    _node._service_clients.append(_service_client)

                ### TODO: action_servers will be supported in future version
                ### TODO: action_clients will be supported in future version

                _app._nodes.append(_node)
            ### TODO: Modules will be supported in future version
            for module_obj in app_obj_i["modules"]:
                _module = WOLfesIRModule()
                _app._modules.append(_module)

            self._ir._apps.append(_app)
            ### check if identifiers repeat
            if self._utils.check_identifier_duplicate(_app._identifiers):
                self._logger.error("app[{}] identifiers duplicate: \n{}".format(i, _app._identifiers))
                raise ValueError("app[{}] identifiers duplicate: \n{}".format(i, _app._identifiers))
            else:
                self._logger.debug("app[{}] all identifiers: {} valid.".format(i, _app._identifiers))

        return self._ir

if __name__ == '__main__':
    parser = BaseConfigParser()
    print(sys.path)
    print(parser.parse_version_string("0.7.0"))
    # print(parser.parse_version_string("v0.7.0"))
    print(parser.parse_version_string("1.07.00.00"))