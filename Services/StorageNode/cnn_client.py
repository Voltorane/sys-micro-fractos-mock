from __future__ import print_function

import logging

import grpc
import sys
sys.path.insert(1, "../ComputationalNodes/CNN/CNN_Controller")
import cnn_controller_pb2_grpc
import cnn_controller_pb2
import base64
import sys

# sys.path.insert(1, "../../../StorageNode")
import storage_service

def run():
    with grpc.insecure_channel('localhost:50051') as channel:       
        stub = cnn_controller_pb2_grpc.PredictorStub(channel)
        img_arr = storage_service.img_to_arr('storage/0.jpg', 128, 128)
        encoded_arr = base64.b64encode(img_arr)
        response = stub.Initialization(cnn_controller_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=128, img_height=128))
        response = stub.Prediction(cnn_controller_pb2.PredictionRequest(image=encoded_arr, img_width=128, img_height=128))
        print("Received prediction: " + str(response.data_class))

if __name__ == '__main__':
    logging.basicConfig()
    run()