# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import cnn_controller_pb2 as cnn__controller__pb2


class PredictorStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Prediction = channel.unary_unary(
                '/cnn_controller.Predictor/Prediction',
                request_serializer=cnn__controller__pb2.PredictionRequest.SerializeToString,
                response_deserializer=cnn__controller__pb2.PredictionResponse.FromString,
                )


class PredictorServicer(object):
    """The greeting service definition.
    """

    def Prediction(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PredictorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Prediction': grpc.unary_unary_rpc_method_handler(
                    servicer.Prediction,
                    request_deserializer=cnn__controller__pb2.PredictionRequest.FromString,
                    response_serializer=cnn__controller__pb2.PredictionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cnn_controller.Predictor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Predictor(object):
    """The greeting service definition.
    """

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
        return grpc.experimental.unary_unary(request, target, '/cnn_controller.Predictor/Prediction',
            cnn__controller__pb2.PredictionRequest.SerializeToString,
            cnn__controller__pb2.PredictionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)