from concurrent import futures
import logging

import grpc
import sys

sys.path.insert(1, "../CNN_Adaptor")
from cnn_adaptor import Adaptor

#goto Services
sys.path.insert(1, "../../..")
import service_rpc_pb2
import service_rpc_pb2_grpc

class Predictor(service_rpc_pb2_grpc.PredictorServicer):
    def __init__(self) -> None:
        super().__init__()
        self.a = Adaptor()
    
    def send_output(self, data):
        with grpc.insecure_channel('localhost:50052') as channel:       
            stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
            response = stub.StoreOutput(service_rpc_pb2.OutputStorageRequest(data=data, name="output.txt"))
            print("Response from output storage: " + str(response.description))
    
    def Prediction (self, request, context):
        response = self.a.handle_request("PREDICT", request.image, request.img_width, request.img_height)
        response_code, label, data_class = response
        if response_code != 0:
            return service_rpc_pb2.PredictionResponse(error_code=response_code)
        # send output to other storage node
        try:
            self.send_output(data_class)
        except:
            print("Output storage was usuccessfull!")
        return service_rpc_pb2.PredictionResponse(label=int(label), data_class=data_class)
    
    def Initialization(self, request, context):
        response_code = self.a.handle_request("INIT", request.sample_limit, request.epochs, request.img_width, request.img_height)
        return service_rpc_pb2.InitResponse(response_code=response_code)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()