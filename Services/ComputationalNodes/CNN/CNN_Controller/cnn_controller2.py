from concurrent import futures
import logging

import grpc
import sys
import enum

sys.path.insert(1, "../CNN_Adaptor")
from cnn_adaptor import Adaptor

#goto Services
sys.path.insert(1, "../../..")
import service_rpc_pb2
import service_rpc_pb2_grpc
from node_types import NodeType

from kazoo.client import KazooClient

import time
from datetime import datetime

cnn_controller_ip = "127.0.0.1:2182"

class Predictor(service_rpc_pb2_grpc.PredictorServicer):
    def __init__(self) -> None:
        super().__init__()
        self.a = Adaptor()
        try:   
            self.zookeeper = KazooClient("127.0.0.2:2184")
            self.server_name = 'cnn_controller2'
            self.server_data = "mariadb://172.16.0.111:3306"
            self.patch_chroot = '/cnn_controller'
            self.path_nodes = "/nodes"
            self.path_data = "/data"

            self.connect()
            self.chroot()
            self.register()
            self.watch_application_nodes()
            self.watch_application_data()
        except:
            pass

    def connect(self):
        self.zookeeper.start()

    def chroot(self):
        self.zookeeper.ensure_path(self.patch_chroot)
        self.zookeeper.chroot = self.patch_chroot

    def register(self):
        self.zookeeper.create("{0}/{1}_".format(self.path_nodes, self.server_name),
                              ephemeral=True, sequence=True, makepath=True)

    def watch_application_data(self):
        self.zookeeper.ensure_path(self.path_data)
        self.zookeeper.DataWatch(path=self.path_data, func=self.check_application_data)

    def watch_application_nodes(self):
        self.zookeeper.ensure_path(self.path_nodes)
        self.zookeeper.ChildrenWatch(path=self.path_nodes, func=self.check_application_nodes)

    def check_application_nodes(self, children):
        application_nodes = [{"node": i[0], "sequence": i[1]} for i in (i.split("_") for i in children)]
        current_leader = min(application_nodes, key=lambda x: x["sequence"])["node"]

        self.display_server_information(application_nodes, current_leader)
        if current_leader == self.server_name:
            self.update_shared_data()

    def check_application_data(self, data, stat):
        print(
            "Data change detected on {0}:\nData: {1}\nStat: {2}".format((datetime.now()).strftime("%B %d, %Y %H:%M:%S"),
                                                                        data, stat))
        print()

    def update_shared_data(self):
        if not self.zookeeper.exists(self.path_data):
            self.zookeeper.create(self.path_data,
                                  bytes("name: {0}\ndata: {1}".format(self.server_name, self.server_data), "utf8"),
                                  ephemeral=True, sequence=False, makepath=True)

    def display_server_information(self, application_nodes, current_leader):
        print("Datetime: {0}".format((datetime.now()).strftime("%B %d, %Y %H:%M:%S")))
        print("Server name: {0}".format(self.server_name))
        print("Nodes:")
        for i in application_nodes:
            print("  - {0} with sequence {1}".format(i["node"], i["sequence"]))
        print("Role: {0}".format("leader" if current_leader == self.server_name else "follower"))
        print()

    def __del__(self):
        self.zookeeper.close()    
    
    # returns next request method and all the keys
    def parse_next_request(self, request):
        request = request.split(",")
        node_type = request[0]
        ip = request[1]
        request = request[2:]
        if node_type == NodeType.OutputCollectorNode.value:
            name, storage_id = "", ""
            for argument in request:
                print(argument)
                argument = argument.split(":")
                key, value = argument[0], argument[1]
                if key == "storage_id":
                        storage_id = value
                elif key == "name":
                        name = value
            return [NodeType.OutputCollectorNode, ip, name, storage_id]
        
        #last call - no further requests
        return None
    
    def send_output(self, data, name, ip, next_request, storage_id=""):
        with grpc.insecure_channel(ip) as channel:       
            stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
            response = stub.StoreOutput(service_rpc_pb2.OutputStorageRequest(data=data, name=name, storage_id=storage_id, next_request=next_request))
            print("Response from output storage: " + str(response.description))
    
    def Prediction (self, request, context):
        response = self.a.handle_request("PREDICT", request.image, request.img_width, request.img_height)
        response_code, label, data_class = response
        if response_code != 0:
            return service_rpc_pb2.PredictionResponse(error_code=response_code)
        # TODO RETRIEVE STORAGE ID
        # send output to other storage node
        print(request.next_request)
        next_request = self.parse_next_request(request.next_request.pop(0))
        req = request.next_request
        if next_request is not None:
            node_type, ip, args = next_request[0], next_request[1], next_request[2:]
            if node_type == NodeType.OutputCollectorNode:
                name, storage_id = args[0], args[1]
            try:
                self.send_output(data_class, name, ip, req, storage_id)
            except:
                print("Output storage was usuccessfull!")
        return service_rpc_pb2.PredictionResponse(label=int(label), data_class=data_class)
    
    def Initialization(self, request, context):
        response_code = self.a.handle_request("INIT", request.sample_limit, request.epochs, request.img_width, request.img_height)
        return service_rpc_pb2.InitResponse(response_code=response_code)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port(cnn_controller_ip)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
    # while True:
        # time.sleep