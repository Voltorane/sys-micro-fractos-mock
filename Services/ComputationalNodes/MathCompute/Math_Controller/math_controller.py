from concurrent import futures
import logging
import getopt

import grpc
import sys
import os
from datetime import datetime

sys.path.insert(1, "../CNN_Adaptor")
from cnn_adaptor import Adaptor

sys.path.insert(1, "../../../")
import zookeeper_service
import kazoo

#goto Services
sys.path.insert(1, "../../..")
import service_rpc_pb2
import service_rpc_pb2_grpc
from utils.node_types import NodeType
from utils import ip_connector

config_dir = "../../../config"
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
math_controller_port = ip_connector.extract_port("math_controller", os.path.join(config_dir, "controller_ports.cfg"))
math_controller_ip = f"{grpc_ip}:{math_controller_port}"

class Math_Calculator(service_rpc_pb2_grpc.PredictorServicer):
    def __init__(self, run_with_zookeeper=False) -> None:
        super().__init__()
        self.a = Adaptor()
        self.name = "math_controller"
        self.dir_path = os.path.dirname(__file__)
        # TODO make argument when running
        self.run_with_zookeeper = run_with_zookeeper
        if self.run_with_zookeeper:
            print("Controller is being run with zookeeper!")
            self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
            # TODO think about giving port config path in the arguments when calling
            self.z_port = ip_connector.extract_port(self.name, os.path.join(config_dir, "zookeeper_controller_ports.cfg"))
            # try connecting to all the ip's from config utill connection is successfull
            if self.z_port is not None:
                for z_ip in self.z_ips:
                    try:
                        self.zookeeper = zookeeper_service.ZKeeper(f"{z_ip}:{self.z_port}", f"{self.name}")
                    except Exception as e:
                        print("Trying to reconnect to different ip...")
                    else:
                        break
        else:
            print("Controller is being run without zookeeper!")
        

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
            response = stub.StorePrediction(service_rpc_pb2.ImageStorageRequest(data=data, name=name, storage_id=storage_id, next_request=next_request))
            print("Response from output storage: " + str(response.description))
    
    def Calculate (self, request, context):
        response = self.a.handle_request("CALCULATE", request.function, request.arg1, request.arg2, request.arg3)
        response_code, label, data_class = response
        if response_code != 0:
            return service_rpc_pb2.PredictionResponse(error_code=response_code)
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

def serve(run_with_zookeeper=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_PredictorServicer_to_server(Predictor(run_with_zookeeper), server)
    server.add_insecure_port(math_controller_ip)
    server.start()
    server.wait_for_termination()

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "z")
    except getopt.GetoptError:
        print("Error by parsing args!")
        return
    run_with_zookeeper = False
    for opt, arg in opts:
        if opt in ('-z, "--zookeeper'):
            run_with_zookeeper = True    
    logging.basicConfig()
    serve(run_with_zookeeper=run_with_zookeeper)

if __name__ == '__main__':
    main(sys.argv)
