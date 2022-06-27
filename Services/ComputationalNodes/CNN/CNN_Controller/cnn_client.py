from __future__ import print_function

import logging

import grpc
import cnn_controller_pb2_grpc
import cnn_controller_pb2
import base64
import sys

sys.path.insert(1, "../../../StorageNode")
import storage_service

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cnn_controller_pb2_grpc.PredictorStub(channel)
        img_arr = storage_service.img_to_arr('0.jpg', 128, 128)
        encoded_arr = base64.b64encode(img_arr)
        response = stub.Prediction(cnn_controller_pb2.PredictionRequest(image=encoded_arr, img_width=128, img_height=128))
        print("Received prediction: " + response.label)

if __name__ == '__main__':
    logging.basicConfig()
    run()