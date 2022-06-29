import logging
import getopt
import grpc
import os
import sys
from datetime import datetime
from concurrent import futures
from sqlalchemy import desc
sys.path.insert(1, "../")
from Storage_Adaptor import storage_adaptor
# goto Services
sys.path.insert(1, "../..")
import service_rpc_pb2_grpc
import service_rpc_pb2
import zookeeper_service
from utils.node_types import NodeType
from utils import ip_connector
from utils.node_types import parse_next_request
from utils.request_wrappers import *
import kazoo
from kazoo.client import KazooClient

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file_output_collector = "logfile_storage_controller_output_collector.log"
log_file_image_sender = "logfile_storage_controller_image_sender.log"

config_dir = "../../config"
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
storage_controller_port = ip_connector.extract_port("storage_controller"
                            , os.path.join(config_dir, "controller_ports.cfg"))
storage_controller_ip = f"{grpc_ip}:{storage_controller_port}"


class OutputCollector(service_rpc_pb2_grpc.OutputCollectorServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
        self.name = "storage_controller"
        self.dir_path = os.path.dirname(__file__)
        self.verbose = verbose
        self.run_with_zookeeper = run_with_zookeeper

        logging.basicConfig(filename=log_file_output_collector, filemode=log_filemode, format=log_format, force=True)
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

    
    def StorePrediction(self, request, context):
        request_name = "STORE"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, description = self.adaptor.handle_request(request_name, request.data, request.name, request.storage_id)

        if response_code == 0:
            self.logger.info("Output storage was successfull!")
        else:
            self.logger.warning(f"Something went wrong: {description}")
        return service_rpc_pb2.Response(response_code=response_code, description=description)
    
    def StoreInt(self, request, context):
        request_name = "STORE"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, description = self.adaptor.handle_request(request_name, request.data, request.name, request.storage_id)

        if response_code == 0:
            self.logger.info("Output storage was successfull!")
        else:
            self.logger.warning("Something went wrong: {description}")
        
        if not len(request.next_request) == 0:
            next_request = parse_next_request(request.next_request.pop(0))
            req = request.next_request
            if next_request is not None:
                node_type, ip, args = next_request[0], next_request[1], next_request[2:]
                if node_type == NodeType.IntSenderNode:
                    return handle_next_request(node_type, ip, req, args, self.logger)
                elif node_type == NodeType.ImageSenderNode:
                    return handle_next_request(node_type, ip, req, args, self.logger)  
        return service_rpc_pb2.Response(response_code=response_code, description=description)

class DataSender(service_rpc_pb2_grpc.DataSenderServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
        self.name = "image_sender"
        self.dir_path = os.path.dirname(__file__)
        self.verbose = verbose
        self.run_with_zookeeper = run_with_zookeeper

        logging.basicConfig(filename=log_file_image_sender, filemode=log_filemode, format=log_format, force=True)
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
        # TODO delete if move to other file
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
    
    def SendImage(self, request, context):
        request_name = "SEND_IMAGE"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, encoded_arr, description = self.adaptor.handle_request(request_name, request.name
                                                    , request.img_width, request.img_height, request.client_id)

        if response_code != 0:
            self.logger.error(f"ERROR something went wrong: {description}")
            return service_rpc_pb2.Response(response_code=response_code, description=description)
        self.logger.info("Sending of image was successfull!")
        next_request = parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.PredictorNode:
                img_width, img_height, client_id = args[0], args[1], args[2]
                return handle_next_request(node_type, ip, req, [encoded_arr, img_width, img_height, client_id], self.logger)
            # nothing to append to the request from this node
            elif node_type == NodeType.IntSenderNode:
                return handle_next_request(node_type, ip, req, args, self.logger)
            elif node_type == NodeType.ImageSenderNode:
                return handle_next_request(node_type, ip, req, args, self.logger)  

    def SendInt(self, request, context):
        request_name = "SEND_INT"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, n, description = self.adaptor.handle_request(request_name, request.name, request.client_id)

        if response_code != 0:
            self.logger.error(f"ERROR something went wrong: {description}")
            return service_rpc_pb2.Response(response_code=response_code, description=description)
        self.logger.info("Sending of int was successfull!")
        print(request)
        next_request = parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.MathComputeNode:
                return handle_next_request(node_type, ip, req, [n], self.logger)
            elif node_type == NodeType.IntSenderNode:
                return handle_next_request(node_type, ip, req, args, self.logger)
            elif node_type == NodeType.ImageSenderNode:
                return handle_next_request(node_type, ip, req, args, self.logger)
                # return send_int_to_math_compute(n, req, ip, self.logger)


def serve(run_with_zookeeper=False, verbose=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_OutputCollectorServicer_to_server(OutputCollector(run_with_zookeeper, verbose), server)
    service_rpc_pb2_grpc.add_DataSenderServicer_to_server(DataSender(run_with_zookeeper, verbose), server)
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
