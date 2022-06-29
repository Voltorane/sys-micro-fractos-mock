from concurrent import futures
import logging
import getopt

import grpc
import sys
import os
from datetime import datetime

dir_path = os.path.dirname(__file__)

sys.path.insert(1, os.path.join(dir_path,"../Math_Adaptor"))
from math_adaptor import Adaptor
sys.path.pop(0)

sys.path.insert(1, os.path.join(dir_path,"../../../"))
import zookeeper_service
import kazoo
sys.path.pop(0)

#goto Services
sys.path.insert(1, os.path.join(dir_path,"../../.."))
import service_rpc_pb2
import service_rpc_pb2_grpc
from utils.node_types import NodeType
from utils.node_types import parse_next_request
from utils.request_wrappers import *
from utils import ip_connector
from utils.controller_arg_parser import *
sys.path.pop(0)

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file = "logfile_math_controller.log"

config_dir = os.path.join(dir_path, "../../../config")
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
math_controller_port = ip_connector.extract_port("math_controller", os.path.join(config_dir, "controller_ports.cfg"))
math_controller_ip = f"{grpc_ip}:{math_controller_port}"

class MathComputer(service_rpc_pb2_grpc.MathComputerServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False, servers=1) -> None:
        super().__init__()
        self.adaptor = Adaptor()
        self.name = "math_controller"
        self.verbose = verbose
        logging.basicConfig(filename=log_file,filemode=log_filemode, format=log_format)
        self.logger = logging.getLogger()
        # prints to console
        if self.verbose:
            consoleHandler = logging.StreamHandler()
            self.logger.addHandler(consoleHandler)
        self.logger.setLevel(logging.INFO)

        self.run_with_zookeeper = run_with_zookeeper
        if self.run_with_zookeeper:
            self.logger.info(f"Controller {self.name} is being run with zookeeper!")
            self.z_ips = ip_connector.extract_ip_list(os.path.join(dir_path, "ips.cfg"))
            # TODO think about giving port config path in the arguments when calling
            self.z_port = ip_connector.extract_port(self.name, os.path.join(config_dir, "zookeeper_controller_ports.cfg"))
            # try connecting to all the ip's from config utill connection is successfull
            for server_id in range(servers):
                if self.z_port is not None:
                    for z_ip in self.z_ips:
                        try:
                            self.zookeeper = zookeeper_service.ZKeeper(f"{z_ip}:{self.z_port}", f"{self.name}", self.logger, server_id)
                        except Exception as e:
                            self.logger.warning("Trying to reconnect to different ip...")
                        else:
                            break
        else:
            self.logger.info(f"Controller {self.name} is being run without zookeeper!")
    
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
            if node_type == NodeType.OutputCollectorNode:
                self.logger.info(f"Passing request to {node_type.name}!")
                name, storage_id = args[0], args[1]
                return handle_next_request(node_type, ip, req, [result, name, storage_id], self.logger)
            elif node_type == NodeType.IntSenderNode:
                self.logger.info(f"Passing request to {node_type.name}!")
                return handle_next_request(node_type, ip, req, args, self.logger)
                
        return service_rpc_pb2.Response(response_code=response_code, description=description)

def serve(run_with_zookeeper=False, verbose=False, servers=1):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_MathComputerServicer_to_server(MathComputer(run_with_zookeeper, verbose, servers), server)
    server.add_insecure_port(math_controller_ip)
    server.start()
    server.wait_for_termination()

def main(argv):
    run_with_zookeeper, verbose, servers = arg_parser(argv)
    serve(run_with_zookeeper=run_with_zookeeper, verbose=verbose, servers=servers)

if __name__ == '__main__':
    main(sys.argv)
