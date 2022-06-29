from concurrent import futures
import logging
import argparse
import getopt

from datetime import datetime
import grpc
import os
#goto StorageNode
import sys

from sqlalchemy import desc
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

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file_output_collector = "logfile_storage_controller_output_collector.log"
log_file_image_sender = "logfile_storage_controller_image_sender.log"

config_dir = "../../config"
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
storage_controller_port = ip_connector.extract_port("storage_controller", os.path.join(config_dir, "controller_ports.cfg"))
storage_controller_ip = f"{grpc_ip}:{storage_controller_port}"

class OutputCollector(service_rpc_pb2_grpc.OutputCollectorServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
        self.name = "storage_controller"
        self.dir_path = os.path.dirname(__file__)
        self.verbose = verbose
        self.run_with_zookeeper = run_with_zookeeper

        logging.basicConfig(filename=log_file_output_collector,filemode=log_filemode, format=log_format)
        self.logger = logging.getLogger()
        # print to console
        if self.verbose:
            consoleHandler = logging.StreamHandler()
            self.logger.addHandler(consoleHandler)
        self.logger.setLevel(logging.INFO)

        if self.run_with_zookeeper:
            self.logger.info(f"Controller {self.name} is being run with zookeeper!")
            self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
            # TODO think about giving port config path in the arguments when calling
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

    
    def StoreOutput(self, request, context):
        request_name = "STORE"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, description = self.adaptor.handle_request(request_name, request.data, request.name, request.storage_id)

        if response_code == 0:
            self.logger.info("Output storage was successfull!")
        else:
            self.logger.error("ERROR something went wrong: {description}")
        return service_rpc_pb2.OutputSotrageResponse(response_code=response_code, description=description)

class ImageSender(service_rpc_pb2_grpc.ImageSenderServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
        self.name = "image_sender"
        self.dir_path = os.path.dirname(__file__)
        self.verbose = verbose
        self.run_with_zookeeper = run_with_zookeeper


        logging.basicConfig(filename=log_file_image_sender,filemode=log_filemode, format=log_format)
        self.logger = logging.getLogger()
        # prints to console
        if self.verbose:
            consoleHandler = logging.StreamHandler()
            self.logger.addHandler(consoleHandler)
        self.logger.setLevel(logging.INFO)

        self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
        # TODO think about giving port config path in the arguments when calling
        self.z_port = ip_connector.extract_port(self.name, os.path.join(config_dir, "zookeeper_controller_ports.cfg"))
        # try connecting to all the ip's from config utill connection is successfull
        #TODO delete if move to other file
        if self.run_with_zookeeper:
            self.logger.info(f"Controller {self.name} is being run with zookeeper!")
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
        self.logger.info(f"Parsing the request: {request}")
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
            self.logger.info(f"Requesting response from {ip}!")  
            stub = service_rpc_pb2_grpc.PredictorStub(channel)
            response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=img_width, img_height=img_height, next_request=next_request))
            response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
            # TODO: if response.response_code != 0:
                # logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
            # else:
                # logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
            self.logger.info(f"Received response from {ip}")
            return response
    
    def SendImage(self, request, context):
        request_name = "SEND"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, encoded_arr, description = self.adaptor.handle_request(request_name, request.name, request.img_width, request.img_height, request.client_id)

        if response_code != 0:
            self.logger.error("ERROR something went wrong: {description}")
            return service_rpc_pb2.Response(response_code=response_code, description=description)
        self.logger.info("Sending of image was successfull!")
        next_request = self.parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.PredictorNode:
                img_width, img_height, client_id = args[0], args[1], args[2]
                return self.send_to_predictor(encoded_arr, img_width, img_height, client_id, req, ip)

def serve(run_with_zookeeper=False,verbose=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_OutputCollectorServicer_to_server(OutputCollector(run_with_zookeeper, verbose), server)
    service_rpc_pb2_grpc.add_ImageSenderServicer_to_server(ImageSender(run_with_zookeeper, verbose), server)
    server.add_insecure_port(storage_controller_ip)
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