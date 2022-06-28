# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import service_rpc_pb2 as service__rpc__pb2


class PredictorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Prediction = channel.unary_unary(
                '/service_connector.Predictor/Prediction',
                request_serializer=service__rpc__pb2.PredictionRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.PredictionResponse.FromString,
                )
        self.Initialization = channel.unary_unary(
                '/service_connector.Predictor/Initialization',
                request_serializer=service__rpc__pb2.InitRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.InitResponse.FromString,
                )


class PredictorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Prediction(self, request, context):
        """Sends a prediction
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Initialization(self, request, context):
        """initializes the CNN with the given parameters
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PredictorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Prediction': grpc.unary_unary_rpc_method_handler(
                    servicer.Prediction,
                    request_deserializer=service__rpc__pb2.PredictionRequest.FromString,
                    response_serializer=service__rpc__pb2.PredictionResponse.SerializeToString,
            ),
            'Initialization': grpc.unary_unary_rpc_method_handler(
                    servicer.Initialization,
                    request_deserializer=service__rpc__pb2.InitRequest.FromString,
                    response_serializer=service__rpc__pb2.InitResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.Predictor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Predictor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Prediction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.Predictor/Prediction',
            service__rpc__pb2.PredictionRequest.SerializeToString,
            service__rpc__pb2.PredictionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Initialization(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.Predictor/Initialization',
            service__rpc__pb2.InitRequest.SerializeToString,
            service__rpc__pb2.InitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class OutputCollectorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StoreOutput = channel.unary_unary(
                '/service_connector.OutputCollector/StoreOutput',
                request_serializer=service__rpc__pb2.OutputStorageRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.OutputSotrageResponse.FromString,
                )


class OutputCollectorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StoreOutput(self, request, context):
        """Send output from computational node to storage node (typically not the sender node)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OutputCollectorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StoreOutput': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreOutput,
                    request_deserializer=service__rpc__pb2.OutputStorageRequest.FromString,
                    response_serializer=service__rpc__pb2.OutputSotrageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.OutputCollector', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OutputCollector(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StoreOutput(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.OutputCollector/StoreOutput',
            service__rpc__pb2.OutputStorageRequest.SerializeToString,
            service__rpc__pb2.OutputSotrageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ImageSenderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendImage = channel.unary_unary(
                '/service_connector.ImageSender/SendImage',
                request_serializer=service__rpc__pb2.ImageSendRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.ImageSendResponse.FromString,
                )


class ImageSenderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageSenderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendImage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendImage,
                    request_deserializer=service__rpc__pb2.ImageSendRequest.FromString,
                    response_serializer=service__rpc__pb2.ImageSendResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.ImageSender', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageSender(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.ImageSender/SendImage',
            service__rpc__pb2.ImageSendRequest.SerializeToString,
            service__rpc__pb2.ImageSendResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
