from concurrent import futures
import logging

from datetime import datetime
import grpc
import os
#goto StorageNode
import sys
sys.path.insert(1, "../")
from Storage_Adaptor import storage_adaptor

#goto Services
sys.path.insert(1, "../..")
import service_rpc_pb2_grpc
import service_rpc_pb2
import zookeeper_service
from utils.node_types import NodeType
from utils import ip_connector
import kazoo
from kazoo.client import KazooClient
storage_controller_ip = "127.0.0.1:2181"

class OutputCollector(service_rpc_pb2_grpc.OutputCollectorServicer):
    def __init__(self) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
        self.name = "storage_controller"
        self.dir_path = os.path.dirname(__file__)
        self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
        # TODO think about giving port config path in the arguments when calling
        self.z_port = ip_connector.extract_port(self.name, "../../zookeeper_controller_ports.cfg")
        # try connecting to all the ip's from config utill connection is successfull
        if self.z_port is not None:
            for z_ip in self.z_ips:
                try:
                    d = datetime.now().strftime("%H:%M:%S")
                    self.zookeeper = zookeeper_service.ZKeeper(f"{z_ip}:{self.z_port}", f"{self.name}{str(d)}")
                except kazoo.interfaces.IHandler.timeout_exception as e:
                    print("Trying to reconnect to different ip...")
                else:
                    break
    
    def StoreOutput(self, request, context):
        response_code, description = self.adaptor.handle_request("STORE", request.data, request.name, request.storage_id)
        if response_code == 0:
            print("Output storage was successfull!")
        else:
            print(description)
        return service_rpc_pb2.OutputSotrageResponse(response_code=response_code, description=description)

class ImageSender(service_rpc_pb2_grpc.ImageSenderServicer):
    def __init__(self) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
        self.name = "storage_controller"
        self.dir_path = os.path.dirname(__file__)
        self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
        # TODO think about giving port config path in the arguments when calling
        self.z_port = ip_connector.extract_port(self.name, "../../zookeeper_controller_ports.cfg")
        # try connecting to all the ip's from config utill connection is successfull
        #TODO delete if move to other file
        self.name = "image_sender"
        if self.z_port is not None:
            for z_ip in self.z_ips:
                try:
                    d = datetime.now().strftime("%H:%M:%S")
                    self.zookeeper = zookeeper_service.ZKeeper(f"{z_ip}:{self.z_port}", f"{self.name}{str(d)}")
                except kazoo.interfaces.IHandler.timeout_exception as e:
                    print("Trying to reconnect to different ip...")
                else:
                    break
    
    # returns next request method and all the keys
    def parse_next_request(self, request):
        request = request.split(",")
        node_type = request[0]
        ip = request[1]
        request = request[2:]
        if node_type == NodeType.PredictorNode.value:
            img_width, img_height, client_id = None, None, ""
            for argument in request:
                print(argument)
                argument = argument.split(":")
                key, value = argument[0], argument[1]
                if key == "img_width":
                        img_width = int(value)
                elif key == "img_height":
                        img_height = int(value)
                elif key == "client_id":
                        client_id = value
            return [NodeType.PredictorNode, ip, img_width, img_height, client_id]
        
        #last call - no further requests
        return None
        # elif node_type == NodeType.OutputCollectorNode:
        #     for argument in request:
        #         pass
        # elif node_type == NodeType.ImageSenderNode:
        #     for argument in request:
        #         pass
    
    def send_to_predictor(self, encoded_arr, img_width, img_height, client_id, next_request, ip):
        with grpc.insecure_channel(ip) as channel:       
            stub = service_rpc_pb2_grpc.PredictorStub(channel)
            response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=img_width, img_height=img_height, next_request=next_request))
            response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
            print("Received prediction: " + str(response.data_class))
            return response
    
    def SendImage(self, request, context):
        encoded_arr = self.adaptor.handle_request("SEND", request.name, request.img_width, request.img_height, request.client_id)
        print(request.next_request)
        next_request = self.parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.PredictorNode:
                img_width, img_height, client_id = args[0], args[1], args[2]
                return self.send_to_predictor(encoded_arr, img_width, img_height, client_id, req, ip)
        return 

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_OutputCollectorServicer_to_server(OutputCollector(), server)
    service_rpc_pb2_grpc.add_ImageSenderServicer_to_server(ImageSender(), server)
    server.add_insecure_port(storage_controller_ip)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()