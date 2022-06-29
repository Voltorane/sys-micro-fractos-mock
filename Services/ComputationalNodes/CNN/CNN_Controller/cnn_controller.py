import logging
import getopt
import grpc
import sys
import os
from datetime import datetime
from concurrent import futures
sys.path.insert(1, "../CNN_Adaptor")
from cnn_adaptor import Adaptor
sys.path.insert(1, "../../../")
import zookeeper_service
# goto Services
sys.path.insert(1, "../../..")
import service_rpc_pb2
import service_rpc_pb2_grpc
from utils.node_types import NodeType
from utils.node_types import parse_next_request
from utils import ip_connector
from utils.request_wrappers import *

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file = "logfile_cnn_controller.log"

config_dir = "../../../config"
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
cnn_controller_port = ip_connector.extract_port("cnn_controller"
                        , os.path.join(config_dir, "controller_ports.cfg"))
cnn_controller_ip = f"{grpc_ip}:{cnn_controller_port}"


class Predictor(service_rpc_pb2_grpc.PredictorServicer):
    def __init__(self, run_with_zookeeper=False, verbose=False) -> None:
        super().__init__()
        self.adaptor = Adaptor()
        self.name = "cnn_controller"
        self.dir_path = os.path.dirname(__file__)
        self.verbose = verbose
        self.run_with_zookeeper = run_with_zookeeper

        logging.basicConfig(filename=log_file, filemode=log_filemode, format=log_format, force=True)
        self.logger = logging.getLogger()
        # prints to console
        if self.verbose:
            consoleHandler = logging.StreamHandler()
            self.logger.addHandler(consoleHandler)
        self.logger.setLevel(logging.INFO)

        if self.run_with_zookeeper:
            self.logger.info(f"Controller {self.name} is being run with zookeeper!")
            self.z_ips = ip_connector.extract_ip_list(os.path.join(self.dir_path, "ips.cfg"))
            # TODO think about giving port config path in the arguments when calling
            self.z_port = ip_connector.extract_port(self.name
                            , os.path.join(config_dir, "zookeeper_controller_ports.cfg"))
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
    
    def Prediction (self, request, context):
        request_name = "PREDICT"
        self.logger.info(f"Received the following request: {request_name}")
        adaptor_response = self.adaptor.handle_request(request_name, request.image, request.img_width, request.img_height)
        
        response_code, label, data_class, description = adaptor_response
        if response_code != 0:
            return service_rpc_pb2.Response(response_code=response_code, desciption=description)
        # send output to other storage node
        # print(request.next_request)
        next_request = parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.OutputCollectorNode:
                name, storage_id = args[0], args[1]
            try:
                send_prediction(data_class, name, ip, req, storage_id, self.logger)
            except:
                self.logger.error("ERROR: output storage was usuccessfull!")
        return service_rpc_pb2.Response(response_code=response_code, description=description)

    def Initialization(self, request, context):
        request_name = "INIT"
        self.logger.info(f"Received the following request: {request_name}")
        response_code, description = self.adaptor.handle_request(request_name, request.sample_limit
                                        , request.epochs, request.img_width, request.img_height)
        return service_rpc_pb2.Response(response_code=response_code, description=description)


def serve(run_with_zookeeper=False, verbose=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_PredictorServicer_to_server(Predictor(run_with_zookeeper, verbose), server)
    server.add_insecure_port(cnn_controller_ip)
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
