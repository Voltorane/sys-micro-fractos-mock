from __future__ import print_function
import logging
import grpc
import sys
from kazoo.client import KazooClient
sys.path.insert(1, "../Services")
import service_rpc_pb2
import service_rpc_pb2_grpc
import zookeeper_service
from datetime import datetime
import time

cnn_controller_ip = "127.0.0.1:2182"
storage_controller_ip = "127.0.0.1:2181"

class Storage_Predictor_Output(object):
    def __init__(self) -> None:
        self.zookeeper = zookeeper_service.ZKeeper("127.0.0.1:2186", "test_app")

def run():
    with grpc.insecure_channel(storage_controller_ip) as channel:       
        stub = service_rpc_pb2_grpc.ImageSenderStub(channel)
        name = "1.jpg"
        client_id = "TEST"
        img_width = 128
        img_height = 128
        next_node = "PREDICTOR"
        output_name = "test_name"
        next_request = [f"PREDICTOR,{cnn_controller_ip},img_width:{img_width},img_height:{img_height},client_id:{client_id}",
                        f"STORAGE,{storage_controller_ip},name:{output_name},storage_id:{client_id}"]
        response = stub.SendImage(service_rpc_pb2.ImageSendRequest(name=name, img_width=img_width, img_height=img_height, client_id=client_id, next_node=next_node, next_request=next_request))
        print("Received response: " + str(response))

if __name__ == '__main__':
    Storage_Predictor_Output()
    logging.basicConfig()
    run()
    