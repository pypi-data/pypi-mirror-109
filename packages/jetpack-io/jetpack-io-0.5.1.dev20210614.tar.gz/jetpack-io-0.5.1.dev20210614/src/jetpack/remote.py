import time
from concurrent import futures
from typing import Callable, NamedTuple

import grpc
import jsonpickle
from jetpack.proto import remote_api_pb2, remote_api_pb2_grpc

# FuncArgs is used by jsonpickle to capture the arguments to a RPC
FuncArgs = NamedTuple("FuncArgs", [("args", tuple), ("kwargs", dict)])


def result_as_proto(result):
    response = remote_api_pb2.RemoteCallResponse()
    response.json_results = jsonpickle.encode(result)
    return response


class Servicer(remote_api_pb2_grpc.RemoteExecutorServicer):
    def __init__(self):
        # TODO: Figure out if we need any locking around the symbol table.
        self.symbol_table = {}  # TODO: lock?

    def Export(self, fn):
        self.symbol_table[fn.__name__] = fn

    def RemoteCall(self, request, context):
        fn = self.symbol_table[request.method_name]
        func_args: FuncArgs = jsonpickle.decode(request.json_args)
        result = fn(*func_args.args, **func_args.kwargs)
        return result_as_proto(result)


class Server:
    def __init__(self):
        self.servicer = Servicer()
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        remote_api_pb2_grpc.add_RemoteExecutorServicer_to_server(
            self.servicer, self.server
        )
        self.is_listening = False  # TODO: Mutex needed?

    def Listen(self):
        self.server.add_insecure_port("[::]:50051")
        self.server.start()
        self.is_listening = True

    def Export(self, fn):
        # Connect to the network lazily
        if not self.is_listening:
            self.Listen()
        self.servicer.Export(fn)


class Client:
    def __init__(self):
        self.address = "localhost:50051"
        self.channel = None
        self.stub = None
        self.is_dialed = False  # TODO: Mutex needed?

    def Dial(self):
        self.channel = grpc.insecure_channel(self.address)
        self.stub = remote_api_pb2_grpc.RemoteExecutorStub(self.channel)
        self.is_dialed = True

    def RemoteCall(self, request):
        # Lazily connect to the network. Putting this here so we get a clean
        # API from the get-go, but in practice we might want to do the network
        # connection when a function is *imported* as a stub, rather than on the
        # actual function call (to reduce latency on the call)
        if not self.is_dialed:
            self.Dial()
        return self.stub.RemoteCall(request)
