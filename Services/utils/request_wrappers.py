import logging
import sys
import os
from threading import Semaphore
from time import sleep
from urllib import response
import grpc
import datetime
from pathlib import Path

from pexpect import TIMEOUT

sys.path.insert(1, os.path.dirname(__file__))
from node_types import NodeType

sys.path.insert(1, "../")
import service_rpc_pb2
import service_rpc_pb2_grpc

TIMEOUT = 5
m = Semaphore(1)

# def acquire():
#     number = 0
#     while number <= 0:
#         with open(os.path.join(Path(__file__).parent.absolute(), "../config/math"), "r") as m:
#             number = int(m.read())
#             print(number)
#         sleep(0.1)
#     with open(os.path.join(Path(__file__).parent.absolute(), "../config/math"), "w") as m:
#             m.write(str(number-1))

# def release():
#     with open(os.path.join(Path(__file__).parent.absolute(), "../config/math"), "r+") as m:
#             number = int(m.read())
#             m.write(str(number+1))
        

def send_request_to_int_sender(name, client_id, next_request, ip, logger=None):
    with grpc.insecure_channel(ip) as channel:
        stub = service_rpc_pb2_grpc.DataSenderStub(channel)
        response = stub.SendInt(service_rpc_pb2.IntSendRequest(name=name, client_id=client_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_request_to_image_sender(name, img_width, img_height, client_id, next_request, ip, logger=None):
    with grpc.insecure_channel(ip) as channel:
        stub = service_rpc_pb2_grpc.DataSenderStub(channel)
        response = stub.SendImage(service_rpc_pb2.ImageSendRequest(name=name, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response


def send_prediction(data, name, ip, next_request, storage_id, logger=None):
    with grpc.insecure_channel(ip) as channel:       
        stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
        response = stub.StorePrediction(service_rpc_pb2.PredictionStorageRequest(data=data, name=name, storage_id=storage_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_int_to_math_compute(n, next_request, ip, logger=None):
    with grpc.insecure_channel(ip) as channel:       
        stub = service_rpc_pb2_grpc.MathComputerStub(channel)
        response = stub.ComputeFact(service_rpc_pb2.ComputeFactRequest(n=n, next_request=next_request))

        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_image_to_predictor(encoded_arr, img_width, img_height, client_id, next_request, ip, logger=None):
    with grpc.insecure_channel(ip) as channel:       
        stub = service_rpc_pb2_grpc.PredictorStub(channel)
        response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=img_width, img_height=img_height, next_request=next_request))
        response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_output(data, name, ip, next_request, storage_id, logger=None):
    with grpc.insecure_channel(ip) as channel:       
        stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
        response = stub.StoreInt(service_rpc_pb2.IntStorageRequest(data=str(data), name=name, storage_id=storage_id, next_request=next_request))
        if logger is not None:
            logger.info("Response from output storage: " + str(response.description))
        else:
            print("Response from output storage: " + str(response.description))
        return response

# math node - n = args[0]
# cnn node - encoded_arr, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
# int sender node - name, client_id = args[0], args[1]
# image sender node - name, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
# output collecter node - data, name, storage_id = args[0], args[1], args[2]
def handle_next_request(node_type, ip, next_request, args, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    start_time = cur_time = int(round(datetime.datetime.now().timestamp() / 1000))
    logger.info(f"Sending request to {ip}!")
    response = None
    while start_time - cur_time < TIMEOUT:
        try:
            if node_type == NodeType.MathComputeNode:
                n = args[0]
                print("1")
                # acquire()
                print("4")
                response = send_int_to_math_compute(n, next_request, ip, logger)
                # release()
            elif node_type == NodeType.PredictorNode:
                encoded_arr, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
                response = send_image_to_predictor(encoded_arr, img_width, img_height, client_id, next_request, ip, logger)
            elif node_type == NodeType.IntSenderNode:
                name, client_id = args[0], args[1]
                response = send_request_to_int_sender(name, client_id, next_request, ip)
            elif node_type == NodeType.ImageSenderNode:
                name, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
                response = send_request_to_image_sender(name, img_width, img_height, client_id, next_request, ip, logger)
            elif node_type == NodeType.OutputCollectorNode:
                data, name, storage_id = args[0], args[1], args[2]
                response = send_output(data, name, ip, next_request, storage_id, logger)
            cur_time = int(round(datetime.datetime.now().timestamp() / 1000))
        except:
            sleep(1)
            logger.info(f"Waiting for response from {node_type}")
        else:
            logger.info(f"Request sucessfully sent {ip}!")
            return response