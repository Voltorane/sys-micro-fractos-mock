from __future__ import print_function
import logging
import grpc
import sys
from kazoo.client import KazooClient
sys.path.insert(1, "../Services")
import service_rpc_pb2
import service_rpc_pb2_grpc
from datetime import datetime
import time

cnn_controller_ip = "127.0.0.1:2182"
storage_controller_ip = "127.0.0.1:2181"

class Storage_Predictor_Output(object):
    def __init__(self) -> None:
        try:
            self.zookeeper = KazooClient(["127.0.0.1:2185","127.0.0.2:2185","127.0.0.3:2185"])

            self.patch_chroot = '/storage_prediction_output'
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
        # encoded_arr = storage_service.img_to_arr('storage/0.jpg', 128, 128)
        # response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=128, img_height=128))
        # response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=128, img_height=128))
        print("Received response: " + str(response))

if __name__ == '__main__':
    Storage_Predictor_Output()
    logging.basicConfig()
    run()
    while True:
        time.sleep