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
                response_deserializer=service__rpc__pb2.Response.FromString,
                )
        self.Initialization = channel.unary_unary(
                '/service_connector.Predictor/Initialization',
                request_serializer=service__rpc__pb2.InitRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
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
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
            'Initialization': grpc.unary_unary_rpc_method_handler(
                    servicer.Initialization,
                    request_deserializer=service__rpc__pb2.InitRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
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
            service__rpc__pb2.Response.FromString,
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
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class OutputCollectorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StorePrediction = channel.unary_unary(
                '/service_connector.OutputCollector/StorePrediction',
                request_serializer=service__rpc__pb2.PredictionStorageRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )
        self.StoreInt = channel.unary_unary(
                '/service_connector.OutputCollector/StoreInt',
                request_serializer=service__rpc__pb2.IntStorageRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )


class OutputCollectorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StorePrediction(self, request, context):
        """Send output from computational node to storage node (typically not the sender node)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StoreInt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OutputCollectorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StorePrediction': grpc.unary_unary_rpc_method_handler(
                    servicer.StorePrediction,
                    request_deserializer=service__rpc__pb2.PredictionStorageRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
            'StoreInt': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreInt,
                    request_deserializer=service__rpc__pb2.IntStorageRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.OutputCollector', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OutputCollector(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StorePrediction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.OutputCollector/StorePrediction',
            service__rpc__pb2.PredictionStorageRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StoreInt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.OutputCollector/StoreInt',
            service__rpc__pb2.IntStorageRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class DataSenderStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendImage = channel.unary_unary(
                '/service_connector.DataSender/SendImage',
                request_serializer=service__rpc__pb2.ImageSendRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )
        self.SendInt = channel.unary_unary(
                '/service_connector.DataSender/SendInt',
                request_serializer=service__rpc__pb2.IntSendRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )


class DataSenderServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendInt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataSenderServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendImage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendImage,
                    request_deserializer=service__rpc__pb2.ImageSendRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
            'SendInt': grpc.unary_unary_rpc_method_handler(
                    servicer.SendInt,
                    request_deserializer=service__rpc__pb2.IntSendRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.DataSender', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataSender(object):
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
        return grpc.experimental.unary_unary(request, target, '/service_connector.DataSender/SendImage',
            service__rpc__pb2.ImageSendRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendInt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.DataSender/SendInt',
            service__rpc__pb2.IntSendRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ApplicationStarterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendInitialRequest = channel.unary_unary(
                '/service_connector.ApplicationStarter/SendInitialRequest',
                request_serializer=service__rpc__pb2.ApplicationInitRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )


class ApplicationStarterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendInitialRequest(self, request, context):
        """starts application
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ApplicationStarterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendInitialRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.SendInitialRequest,
                    request_deserializer=service__rpc__pb2.ApplicationInitRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.ApplicationStarter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ApplicationStarter(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendInitialRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.ApplicationStarter/SendInitialRequest',
            service__rpc__pb2.ApplicationInitRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class MathComputerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ComputeFact = channel.unary_unary(
                '/service_connector.MathComputer/ComputeFact',
                request_serializer=service__rpc__pb2.ComputeFactRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )
        self.ComputeBinom = channel.unary_unary(
                '/service_connector.MathComputer/ComputeBinom',
                request_serializer=service__rpc__pb2.ComputeBinomRequest.SerializeToString,
                response_deserializer=service__rpc__pb2.Response.FromString,
                )


class MathComputerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ComputeFact(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ComputeBinom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MathComputerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ComputeFact': grpc.unary_unary_rpc_method_handler(
                    servicer.ComputeFact,
                    request_deserializer=service__rpc__pb2.ComputeFactRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
            'ComputeBinom': grpc.unary_unary_rpc_method_handler(
                    servicer.ComputeBinom,
                    request_deserializer=service__rpc__pb2.ComputeBinomRequest.FromString,
                    response_serializer=service__rpc__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'service_connector.MathComputer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MathComputer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ComputeFact(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.MathComputer/ComputeFact',
            service__rpc__pb2.ComputeFactRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ComputeBinom(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/service_connector.MathComputer/ComputeBinom',
            service__rpc__pb2.ComputeBinomRequest.SerializeToString,
            service__rpc__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
