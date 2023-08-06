from typing import Callable, NamedTuple

import grpc
import jsonpickle
from jetpack import remote
from jetpack.proto import remote_api_pb2, remote_api_pb2_grpc

SERVER = remote.Server()
CLIENT = remote.Client()


def export(fn: Callable):
    SERVER.Export(fn)


def function(symbol: str):
    def func_stub(*args, **kwargs):
        request = call_as_proto(symbol, args, kwargs)
        response = remote_call(request)
        return result_from_proto(response)

    return func_stub


# FuncArgs is used by jsonpickle to capture the arguments to a RPC
FuncArgs = NamedTuple("FuncArgs", [("args", tuple), ("kwargs", dict)])


def args_as_json(args, kwargs):
    return jsonpickle.encode(FuncArgs(args=args, kwargs=kwargs))


def call_as_proto(name, args, kwargs):
    request = remote_api_pb2.RemoteCallRequest()
    request.method_name = name
    request.json_args = args_as_json(args, kwargs)
    return request


def result_as_proto(result):
    response = remote_api_pb2.RemoteCallResponse()
    response.json_results = jsonpickle.encode(result)
    return response


def result_from_proto(response):
    return jsonpickle.decode(response.json_results)


def remote_call(request):  # Emulate grpc call
    return CLIENT.RemoteCall(request)
