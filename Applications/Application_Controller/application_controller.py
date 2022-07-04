from concurrent import futures
import logging
import os
import sys

dir_path = os.path.dirname(__file__)

service_dir = os.path.join(dir_path,"../../Services")
sys.path.insert(1, service_dir)
import grpc
import service_rpc_pb2
import service_rpc_pb2_grpc
import zookeeper_service
sys.path.pop(0)

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file = "logfile_app_controller.log"
# logger = logging.getLogger()

util_dir = os.path.join(dir_path,"../../Services/utils")
sys.path.insert(1, util_dir)
import ip_connector
from node_types import NodeType
from node_types import parse_next_request
from request_wrappers import *
from controller_arg_parser import *
sys.path.pop(0)

config_dir = os.path.join(service_dir, "config")
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
application_controller_port = ip_connector.extract_port("application_controller", os.path.join(config_dir, "controller_ports.cfg"))
application_controller_ip = f"{grpc_ip}:{application_controller_port}"

class ApplicationStarter(service_rpc_pb2_grpc.ApplicationStarterServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False, name="") -> None:
        super().__init__()
        self.name = "application_controller"
        self.verbose = verbose
        self.run_with_zookeeper = run_with_zookeeper

        logging.basicConfig(filename=log_file,filemode=log_filemode, format=log_format)
        self.logger = logging.getLogger()
        # prints to console
        if self.verbose:
            consoleHandler = logging.StreamHandler()
            self.logger.addHandler(consoleHandler)
        self.logger.setLevel(logging.INFO)

        if self.run_with_zookeeper:
            self.logger.info(f"Controller {self.name} is being run with zookeeper!")
            self.z_ips = ip_connector.extract_ip_list(os.path.join(dir_path, "ips.cfg"))
            self.z_port = ip_connector.extract_port(self.name, os.path.join(config_dir, "zookeeper_controller_ports.cfg"))
            # try connecting to all the ip's from config utill connection is successfull
            if self.z_port is not None:
                for z_ip in self.z_ips:
                    try:
                        self.zookeeper = zookeeper_service.ZKeeper(f"{z_ip}:{self.z_port}", f"{self.name}", self.logger, name)
                    except Exception as e:
                        self.logger.warning("Trying to reconnect to different ip...")
                    else:
                        break
        else:
            self.logger.info(f"Controller {self.name} is being run without zookeeper!")
    
    def SendInitialRequest(self, request, context):
        # parse next request from the task graph
        # self.logger.info(f"Received the following request: {request}")
        if len(request.request) != 0:
            next_request = parse_next_request(request.request.pop(0))
            req = request.request
            if next_request is not None:
                node_type, ip, args = next_request[0], next_request[1], next_request[2:]
                if node_type == NodeType.ImageSenderNode:
                    # name, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
                    self.logger.info(f"Passing request to {node_type.name}!")
                    return handle_next_request(node_type, ip, req, args, self.logger)
                elif node_type == NodeType.IntSenderNode:
                    # name, client_id = args[0], args[1]
                    self.logger.info(f"Passing request to {node_type.name}!")
                    return handle_next_request(node_type, ip, req, args, self.logger)
                    # return send_request_to_int_sender(name, client_id, req, ip, self.logger)
            else:
                self.logger.info("No further requests!")
        return service_rpc_pb2.Response(response_code=0, description="OK")

def serve(run_with_zookeeper=False, verbose=False, name=""):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_ApplicationStarterServicer_to_server(ApplicationStarter(run_with_zookeeper, verbose, name), server)
    server.add_insecure_port(application_controller_ip)
    server.start()
    server.wait_for_termination()

def main(argv):
    run_with_zookeeper, verbose, name = arg_parser(argv)
    serve(run_with_zookeeper=run_with_zookeeper, verbose=verbose, name=name)

if __name__ == '__main__':
    main(sys.argv)