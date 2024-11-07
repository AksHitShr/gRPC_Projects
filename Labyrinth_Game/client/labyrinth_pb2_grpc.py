# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import labyrinth_pb2 as labyrinth__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in labyrinth_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class LabyrinthGameStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetLabyrinthInfo = channel.unary_unary(
                '/labyrinth.LabyrinthGame/GetLabyrinthInfo',
                request_serializer=labyrinth__pb2.EmptyRequest.SerializeToString,
                response_deserializer=labyrinth__pb2.LabyrinthInfo.FromString,
                _registered_method=True)
        self.GetPlayerStatus = channel.unary_unary(
                '/labyrinth.LabyrinthGame/GetPlayerStatus',
                request_serializer=labyrinth__pb2.EmptyRequest.SerializeToString,
                response_deserializer=labyrinth__pb2.PlayerStatus.FromString,
                _registered_method=True)
        self.RegisterMove = channel.unary_unary(
                '/labyrinth.LabyrinthGame/RegisterMove',
                request_serializer=labyrinth__pb2.MoveRequest.SerializeToString,
                response_deserializer=labyrinth__pb2.MoveResponse.FromString,
                _registered_method=True)
        self.Revelio = channel.unary_stream(
                '/labyrinth.LabyrinthGame/Revelio',
                request_serializer=labyrinth__pb2.RevelioRequest.SerializeToString,
                response_deserializer=labyrinth__pb2.Position.FromString,
                _registered_method=True)
        self.Bombarda = channel.stream_unary(
                '/labyrinth.LabyrinthGame/Bombarda',
                request_serializer=labyrinth__pb2.Position.SerializeToString,
                response_deserializer=labyrinth__pb2.EmptyResponse.FromString,
                _registered_method=True)


class LabyrinthGameServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetLabyrinthInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPlayerStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterMove(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Revelio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Bombarda(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LabyrinthGameServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetLabyrinthInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLabyrinthInfo,
                    request_deserializer=labyrinth__pb2.EmptyRequest.FromString,
                    response_serializer=labyrinth__pb2.LabyrinthInfo.SerializeToString,
            ),
            'GetPlayerStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPlayerStatus,
                    request_deserializer=labyrinth__pb2.EmptyRequest.FromString,
                    response_serializer=labyrinth__pb2.PlayerStatus.SerializeToString,
            ),
            'RegisterMove': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterMove,
                    request_deserializer=labyrinth__pb2.MoveRequest.FromString,
                    response_serializer=labyrinth__pb2.MoveResponse.SerializeToString,
            ),
            'Revelio': grpc.unary_stream_rpc_method_handler(
                    servicer.Revelio,
                    request_deserializer=labyrinth__pb2.RevelioRequest.FromString,
                    response_serializer=labyrinth__pb2.Position.SerializeToString,
            ),
            'Bombarda': grpc.stream_unary_rpc_method_handler(
                    servicer.Bombarda,
                    request_deserializer=labyrinth__pb2.Position.FromString,
                    response_serializer=labyrinth__pb2.EmptyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'labyrinth.LabyrinthGame', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('labyrinth.LabyrinthGame', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class LabyrinthGame(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetLabyrinthInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/labyrinth.LabyrinthGame/GetLabyrinthInfo',
            labyrinth__pb2.EmptyRequest.SerializeToString,
            labyrinth__pb2.LabyrinthInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPlayerStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/labyrinth.LabyrinthGame/GetPlayerStatus',
            labyrinth__pb2.EmptyRequest.SerializeToString,
            labyrinth__pb2.PlayerStatus.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RegisterMove(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/labyrinth.LabyrinthGame/RegisterMove',
            labyrinth__pb2.MoveRequest.SerializeToString,
            labyrinth__pb2.MoveResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Revelio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/labyrinth.LabyrinthGame/Revelio',
            labyrinth__pb2.RevelioRequest.SerializeToString,
            labyrinth__pb2.Position.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Bombarda(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/labyrinth.LabyrinthGame/Bombarda',
            labyrinth__pb2.Position.SerializeToString,
            labyrinth__pb2.EmptyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
