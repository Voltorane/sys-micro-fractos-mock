from __future__ import print_function
import logging
import grpc
import sys
import os
from kazoo.client import KazooClient
from pathlib import Path
dir_path = Path(__file__).parent.absolute()

sys.path.insert(1, os.path.join("../Services"))
import service_rpc_pb2
import service_rpc_pb2_grpc
import zookeeper_service

util_dir = os.path.join(dir_path, "../Services/utils")
sys.path.insert(1, util_dir)
import ip_connector

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file = "logfile_application.log"

config_dir = os.path.join(dir_path, os.path.join("../Services", "config"))
grpc_ip = ip_connector.get_grpc_ip(os.path.join(config_dir, "grpc_ip.cfg"))
storage_controller_port = ip_connector.extract_port("storage_controller"
                            , os.path.join(config_dir, "controller_ports.cfg"))
storage_controller_ip = f"{grpc_ip}:{storage_controller_port}"
math_controller_port = ip_connector.extract_port("math_controller", os.path.join(config_dir, "controller_ports.cfg"))
math_controller_ip = f"{grpc_ip}:{math_controller_port}"
cnn_controller_port = ip_connector.extract_port("cnn_controller"
                        , os.path.join(config_dir, "controller_ports.cfg"))
cnn_controller_ip = f"{grpc_ip}:{cnn_controller_port}"
application_controller_port = ip_connector.extract_port("application_controller", os.path.join(config_dir, "controller_ports.cfg"))
application_controller_ip = f"{grpc_ip}:{application_controller_port}"

class Application(object):
    def __init__(self, run_with_zookeeper=True) -> None:
        logging.basicConfig(filename=log_file,filemode=log_filemode, format=log_format)
        self.logger = logging.getLogger()
        # prints to console
        self.logger.setLevel(logging.INFO)
        self.dir_path = os.path.dirname(__file__)
        self.name = "application"
        if run_with_zookeeper:
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

    def run(self):
        with grpc.insecure_channel(application_controller_ip) as channel:       
            stub = service_rpc_pb2_grpc.ApplicationStarterStub(channel)
            # ------------------------------------TODO------------------------------------------------
            # change the request for the needs of your application
            
            # Request can hold following elements:
            # f"IMAGE_SENDER,{storage_controller_ip},name:{name},img_width:{img_width},img_height:{img_height},client_id:{client_id}"
            # f"PREDICTOR,{cnn_controller_ip},img_width:{img_width},img_height:{img_height},client_id:{client_id}"
            # f"STORAGE,{storage_controller_ip},name:{output_name},storage_id:{client_id}"
            # f"INT_SENDER,{storage_controller_ip},name:{number_name},client_id:{client_id}"
            # f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}"
            request = [] # <--- add your messages here
            # ------------------------------------------------------------------------------------------
            response = stub.SendInitialRequest(service_rpc_pb2.ApplicationInitRequest(request=request))
            self.logger.info(response)

if __name__ == '__main__':
    app = Application()
    logging.basicConfig()
    app.run()