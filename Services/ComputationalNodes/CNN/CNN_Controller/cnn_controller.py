from concurrent import futures
import logging

import grpc
import sys

sys.path.insert(1, "../CNN_Adaptor")
from cnn_adaptor import Adaptor

sys.path.insert(1, "../../../")
import zookeeper_service

#goto Services
sys.path.insert(1, "../../..")
import service_rpc_pb2
import service_rpc_pb2_grpc
from utils.node_types import NodeType


cnn_controller_ip = "127.0.0.1:2182"

class Predictor(service_rpc_pb2_grpc.PredictorServicer):
    def __init__(self) -> None:
        super().__init__()
        self.a = Adaptor()
        self.zookeeper = zookeeper_service.ZKeeper("127.0.0.1:2184", "test_cnn")

    # returns next request method and all the keys
    def parse_next_request(self, request):
        request = request.split(",")
        node_type = request[0]
        ip = request[1]
        request = request[2:]
        if node_type == NodeType.OutputCollectorNode.value:
            name, storage_id = "", ""
            for argument in request:
                print(argument)
                argument = argument.split(":")
                key, value = argument[0], argument[1]
                if key == "storage_id":
                        storage_id = value
                elif key == "name":
                        name = value
            return [NodeType.OutputCollectorNode, ip, name, storage_id]
        
        #last call - no further requests
        return None
    
    def send_output(self, data, name, ip, next_request, storage_id=""):
        with grpc.insecure_channel(ip) as channel:       
            stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
            response = stub.StoreOutput(service_rpc_pb2.OutputStorageRequest(data=data, name=name, storage_id=storage_id, next_request=next_request))
            print("Response from output storage: " + str(response.description))
    
    def Prediction (self, request, context):
        response = self.a.handle_request("PREDICT", request.image, request.img_width, request.img_height)
        response_code, label, data_class = response
        if response_code != 0:
            return service_rpc_pb2.PredictionResponse(error_code=response_code)
        # TODO RETRIEVE STORAGE ID
        # send output to other storage node
        print(request.next_request)
        next_request = self.parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.OutputCollectorNode:
                name, storage_id = args[0], args[1]
            try:
                self.send_output(data_class, name, ip, req, storage_id)
            except:
                print("Output storage was usuccessfull!")
        return service_rpc_pb2.PredictionResponse(label=int(label), data_class=data_class)
    
    def Initialization(self, request, context):
        response_code = self.a.handle_request("INIT", request.sample_limit, request.epochs, request.img_width, request.img_height)
        return service_rpc_pb2.InitResponse(response_code=response_code)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port(cnn_controller_ip)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
