from concurrent import futures
import logging
import getopt

import grpc
import sys
import os
from datetime import datetime

sys.path.insert(1, "../Math_Adaptor")
from math_adaptor import Adaptor

sys.path.insert(1, "../../../")
import zookeeper_service
import kazoo

#goto Services
sys.path.insert(1, "../../..")
import service_rpc_pb2
import service_rpc_pb2_grpc
from utils.node_types import NodeType
from utils.node_types import parse_next_request
from utils.request_wrappers import *
from utils import ip_connector

config_dir = "../../../config"
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
math_controller_port = ip_connector.extract_port("math_controller", os.path.join(config_dir, "controller_ports.cfg"))
math_controller_ip = f"{grpc_ip}:{math_controller_port}"

class MathComputer(service_rpc_pb2_grpc.MathComputerServicer):
    def __init__(self, run_with_zookeeper=False) -> None:
        super().__init__()
        self.adaptor = Adaptor()
        self.name = "math_controller"
        self.dir_path = os.path.dirname(__file__)
        self.logger = None #TODO LOGGER

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
        
    
    # def send_math_output(self, data, name, ip, next_request, storage_id=""):
    #     with grpc.insecure_channel(ip) as channel:       
    #         stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
    #         response = stub.StoreInt(service_rpc_pb2.IntStorageRequest(data=data, name=name, storage_id=storage_id, next_request=next_request))
    #         print("Response from output storage: " + str(response.description))
    #         return response
    
    # def send_request_to_int_sender(self, name, client_id, next_request, ip):
    #     with grpc.insecure_channel(ip) as channel:
    #         self.logger.info(f"Sending request to {ip}!")
    #         stub = service_rpc_pb2_grpc.DataSenderStub(channel)
    #         stub = service_rpc_pb2_grpc.DataSenderStub(channel)
    #         response = stub.SendInt(service_rpc_pb2.IntSendRequest(name=name, client_id=client_id, next_request=next_request))
    #         # response = stub.SendInt(service_rpc_pb2.IntSendRequest(name=name, client_id=client_id, next_request=next_request))
    #         if response.response_code != 0:
    #             self.logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
    #         else:
    #             self.logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
    #         return response
    
    def ComputeFact(self, request, context):
        response = self.adaptor.handle_request("COMPUTE_FAC", request.n)
        response_code, result, description = response
        if response_code != 0:
            return service_rpc_pb2.Response(response_code=response_code, description=description)
        # send output to other storage node
        next_request = parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            print(node_type, args)
            if node_type == NodeType.OutputCollectorNode:
                name, storage_id = args[0], args[1]
                return handle_next_request(node_type, ip, req, [result, name, storage_id], self.logger)
                # try:
                #     return send_output(result, name, ip, req, storage_id, self.logger)
                # except:
                #     print("Output storage was usuccessfull!")
            elif node_type == NodeType.IntSenderNode:
                # name, client_id = args[0], args[1]
                return handle_next_request(node_type, ip, req, args, self.logger)
                # return self.send_request_to_int_sender(name, client_id, req, ip)
                
        return service_rpc_pb2.Response(response_code=response_code, description=description)

def serve(run_with_zookeeper=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_MathComputerServicer_to_server(MathComputer(run_with_zookeeper), server)
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
