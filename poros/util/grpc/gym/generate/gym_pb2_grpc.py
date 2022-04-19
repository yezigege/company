# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gym_pb2 as gym__pb2


class GymStub(object):
    """健身房
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BodyBuilding = channel.unary_unary(
                '/lightweight.Gym/BodyBuilding',
                request_serializer=gym__pb2.Person.SerializeToString,
                response_deserializer=gym__pb2.Reply.FromString,
                )


class GymServicer(object):
    """健身房
    """

    def BodyBuilding(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GymServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'BodyBuilding': grpc.unary_unary_rpc_method_handler(
                    servicer.BodyBuilding,
                    request_deserializer=gym__pb2.Person.FromString,
                    response_serializer=gym__pb2.Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'lightweight.Gym', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Gym(object):
    """健身房
    """

    @staticmethod
    def BodyBuilding(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lightweight.Gym/BodyBuilding',
            gym__pb2.Person.SerializeToString,
            gym__pb2.Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
