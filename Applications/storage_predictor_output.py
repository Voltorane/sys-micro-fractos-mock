from __future__ import print_function
import logging
import grpc
import sys
import os
from kazoo.client import KazooClient
sys.path.insert(1, "../Services")
import service_rpc_pb2
import service_rpc_pb2_grpc
import zookeeper_service

util_dir = "../Services/utils"
sys.path.insert(1, util_dir)
import ip_connector

cnn_controller_ip = "127.0.0.1:2182"
storage_controller_ip = "127.0.0.1:2181"
application_controller_ip = "127.0.0.1:2183"
math_controller_ip = "127.0.0.1:2184"

log_filemode = "a"
log_format = "%(levelname)s %(asctime)s - %(message)s"
log_file = "logfile_cnn_controller.log"

config_dir = os.path.join("../Services", "config")

class Storage_Predictor_Output(object):
    def __init__(self, run_with_zookeeper=True) -> None:
        logging.basicConfig(filename=log_file,filemode=log_filemode, format=log_format)
        self.logger = logging.getLogger()
        # prints to console
        self.logger.setLevel(logging.INFO)
        self.dir_path = os.path.dirname(__file__)
        self.name = "application"
        # self.zookeeper = zookeeper_service.ZKeeper("127.0.0.1:2186", "test_app", self.logger)
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

def run():
    with grpc.insecure_channel(application_controller_ip) as channel:       
        stub = service_rpc_pb2_grpc.ApplicationStarterStub(channel)
        name = "cat_image.jpg"
        client_id = "admin"
        img_width = 128
        img_height = 128
        output_name = name.replace(".jpg", "_")+"class.txt"
        number_name = "number"
        output_name1 = "fac_output1"
        output_name2 = "fac_fac_output1"
        output_name3 = "fac_fac_fac_output1"
        request = [f"IMAGE_SENDER,{storage_controller_ip},name:{name},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
                        f"PREDICTOR,{cnn_controller_ip},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
                        f"STORAGE,{storage_controller_ip},name:{output_name},storage_id:{client_id}",
                        # next request
                        f"INT_SENDER,{storage_controller_ip},name:{number_name},client_id:{client_id}",
                        f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}",
                        f"STORAGE,{storage_controller_ip},name:{output_name1},storage_id:{client_id}",
                        # give previous result as input
                        f"INT_SENDER,{storage_controller_ip},name:{output_name1},client_id:{client_id}",
                        f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}",
                        f"STORAGE,{storage_controller_ip},name:{output_name2},storage_id:{client_id}",
                        # give previous result as input
                        f"INT_SENDER,{storage_controller_ip},name:{output_name2},client_id:{client_id}",
                        f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}",
                        f"STORAGE,{storage_controller_ip},name:{output_name3},storage_id:{client_id}"]
        response = stub.SendInitialRequest(service_rpc_pb2.ApplicationInitRequest(request=request))
        # stub = service_rpc_pb2_grpc.ApplicationStarterStub(channel)
        # name = "cat_image.jpg"
        # client_id = "admin"
        # img_width = 128
        # img_height = 128
        # output_name = name.replace(".jpg", "_")+"class.txt"
        # request = [f"INT_SENDER,{storage_controller_ip},name:{name},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
        #                 f"PREDICTOR,{cnn_controller_ip},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
        #                 f"STORAGE,{storage_controller_ip},name:{output_name},storage_id:{client_id}"]
        # response = stub.SendInitialRequest(service_rpc_pb2.ApplicationInitRequest(request=request))
        # print("Received response: " + str(response))
        
        # stub = service_rpc_pb2_grpc.ApplicationStarterStub(channel)
        # name = "dog_image.jpg"
        # client_id = "admin"
        # img_width = 128
        # img_height = 128
        # output_name = name.replace(".jpg", "_")+"class.txt"
        # request = [f"INT_SENDER,{storage_controller_ip},name:{name},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
        #                 f"PREDICTOR,{cnn_controller_ip},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
        #                 f"STORAGE,{storage_controller_ip},name:{output_name},storage_id:{client_id}"]
        # response = stub.SendInitialRequest(service_rpc_pb2.ApplicationInitRequest(request=request))
        # print("Received response: " + str(response))
        # name = "number"
        # client_id = "admin"
        # # img_width = 128
        # # img_height = 128
        # output_name1 = "fac_output"
        # output_name2 = "fac_fac_output"
        # output_name3 = "fac_fac_fac_output"
        # request = [f"INT_SENDER,{storage_controller_ip},name:{name},client_id:{client_id}",
        #             f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}",
        #             f"STORAGE,{storage_controller_ip},name:{output_name1},storage_id:{client_id}",
        #             # give previous result as input
        #             f"INT_SENDER,{storage_controller_ip},name:{output_name1},client_id:{client_id}",
        #             f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}",
        #             f"STORAGE,{storage_controller_ip},name:{output_name2},storage_id:{client_id}",
        #             # give previous result as input
        #             f"INT_SENDER,{storage_controller_ip},name:{output_name2},client_id:{client_id}",
        #             f"MATH_COMPUTE,{math_controller_ip},client_id:{client_id}",
        #             f"STORAGE,{storage_controller_ip},name:{output_name3},storage_id:{client_id}"]
        # response = stub.SendInitialRequest(service_rpc_pb2.ApplicationInitRequest(request=request))
        # print("Received response: " + str(response))

if __name__ == '__main__':
    Storage_Predictor_Output()
    logging.basicConfig()
    run()
    