from concurrent import futures
import logging

import grpc
import cnn_controller_pb2
import cnn_controller_pb2_grpc
import sys

sys.path.insert(1, "../CNN_Adaptor")
from cnn_adaptor import Adaptor

class Predictor(cnn_controller_pb2_grpc.PredictorServicer):
    def __init__(self) -> None:
        super().__init__()
        self.a = Adaptor()
    
    def send_output(self, text):
        with grpc.insecure_channel('localhost:50052') as channel:       
            stub = cnn_controller_pb2_grpc.OutputCollectorStub(channel)
            # response = stub.Initialization(cnn_controller_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=128, img_height=128))
            response = stub.StoreOutput(cnn_controller_pb2.OutputStorageRequest(text=text))
            print("Response from output storage: " + str(response.description))
    
    def Prediction (self, request, context):
        response = self.a.handle_request("PREDICT", request.image, request.img_width, request.img_height)
        response_code, label, data_class = response
        if response_code != 0:
            return cnn_controller_pb2.PredictionResponse(error_code=response_code)
        self.send_output(data_class)
        return cnn_controller_pb2.PredictionResponse(label=int(label), data_class=data_class)
    
    def Initialization(self, request, context):
        response_code = self.a.handle_request("INIT", request.sample_limit, request.epochs, request.img_width, request.img_height)
        return cnn_controller_pb2.InitResponse(response_code=response_code)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cnn_controller_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()