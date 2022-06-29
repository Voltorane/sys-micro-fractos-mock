from concurrent import futures
import logging
import os
import sys
from urllib import response

service_dir = "../../Services"
sys.path.insert(1, service_dir)
import getopt
import grpc
import service_rpc_pb2
import service_rpc_pb2_grpc
import zookeeper_service

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file = "logfile_app_controller.log"
# logger = logging.getLogger()

util_dir = "../../Services/utils"
sys.path.insert(1, util_dir)
import ip_connector
from node_types import NodeType

# # TODO delete after
# from ...Services import service_rpc_pb2
# from ...Services import service_rpc_pb2_grpc

config_dir = os.path.join(service_dir, "config")
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
application_controller_port = ip_connector.extract_port("application_controller", os.path.join(config_dir, "controller_ports.cfg"))
application_controller_ip = f"{grpc_ip}:{application_controller_port}"

class ApplicationStarter(service_rpc_pb2_grpc.ApplicationStarterServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False) -> None:
        super().__init__()
        self.name = "application_controller"
        self.dir_path = os.path.dirname(__file__)
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
            self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
            self.z_port = ip_connector.extract_port(self.name, os.path.join(config_dir, "zookeeper_controller_ports.cfg"))
            # try connecting to all the ip's from config utill connection is successfull
            if self.z_port is not None:
                for z_ip in self.z_ips:
                    try:
                        self.zookeeper = zookeeper_service.ZKeeper(f"{z_ip}:{self.z_port}", f"{self.name}", self.logger)
                    except Exception as e:
                        self.logger.warning("Trying to reconnect to different ip...")
                    else:
                        break
        else:
            self.logger.info(f"Controller {self.name} is being run without zookeeper!")
        
    # returns next request method and all the keys
    def parse_next_request(self, request):
        self.logger.info("Parsing the request...")
        request = request.split(",")
        node_type = request[0]
        ip = request[1]
        request = request[2:]
        if node_type == NodeType.ImageSenderNode.value:
            img_width, img_height, client_id, name = None, None, "", ""
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
                elif key == "name":
                        name = value
            return [NodeType.ImageSenderNode, ip, name, img_width, img_height, client_id]
    
    def send_request_to_image_sender(self, name, img_width, img_height, client_id, next_request, ip):
        with grpc.insecure_channel(ip) as channel:
            self.logger.info(f"Requesting response from {ip}!")
            stub = service_rpc_pb2_grpc.ImageSenderStub(channel)
            response = stub.SendImage(service_rpc_pb2.ImageSendRequest(name=name, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
            if response.response_code != 0:
                self.logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
            else:
                self.logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
            return response
    
    def SendInitialRequest(self, request, context):
        # parse next request from the task graph
        self.logger.info(f"Received the following request: {request}")
        if len(request.request) != 0:
            next_request = self.parse_next_request(request.request.pop(0))
            req = request.request
            if next_request is not None:
                node_type, ip, args = next_request[0], next_request[1], next_request[2:]
                if node_type == NodeType.ImageSenderNode:
                    name, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
                    self.send_request_to_image_sender(name, img_width, img_height, client_id, req, ip)
            else:
                self.logger.info("No further requests!")
        return service_rpc_pb2.ApplicationInitResponse(response_code=0, description="OK")

def serve(run_with_zookeeper=False, verbose=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_ApplicationStarterServicer_to_server(ApplicationStarter(run_with_zookeeper, verbose), server)
    server.add_insecure_port(application_controller_ip)
    server.start()
    server.wait_for_termination()

def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'zv')
    except getopt.GetoptError:
        print(f"ERROR by parsing args: {argv}!")
    run_with_zookeeper = False
    verbose = False
    for opt, arg in opts:
        if opt in ('-z', '--zookeeper'):
            run_with_zookeeper = True
        if opt in ('-v', '--verbose'):
            verbose = True   
    serve(run_with_zookeeper=run_with_zookeeper, verbose=verbose)

if __name__ == '__main__':
    main(sys.argv)