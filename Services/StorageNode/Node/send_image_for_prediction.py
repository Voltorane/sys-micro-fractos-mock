from __future__ import print_function

import logging

import grpc
import sys
import storage_service

#goto Services
sys.path.insert(1, "../..")
import service_rpc_pb2_grpc
import service_rpc_pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:       
        stub = service_rpc_pb2_grpc.PredictorStub(channel)
        encoded_arr = storage_service.img_to_arr('storage/0.jpg', 128, 128)
        response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=128, img_height=128))
        response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=128, img_height=128))
        print("Received prediction: " + str(response.data_class))

if __name__ == '__main__':
    logging.basicConfig()
    run()