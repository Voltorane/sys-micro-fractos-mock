import logging
import sys
import os
from time import sleep
import grpc
import datetime

from pexpect import TIMEOUT

sys.path.insert(1, os.path.dirname(__file__))
from node_types import NodeType

sys.path.insert(1, "../")
import service_rpc_pb2
import service_rpc_pb2_grpc

TIMEOUT = 5

def send_request_to_int_sender(name, client_id, next_request, ip, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    with grpc.insecure_channel(ip) as channel:
        logger.info(f"Sending request to {ip}!")
        stub = service_rpc_pb2_grpc.DataSenderStub(channel)
        response = stub.SendInt(service_rpc_pb2.IntSendRequest(name=name, client_id=client_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_request_to_image_sender(name, img_width, img_height, client_id, next_request, ip, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    with grpc.insecure_channel(ip) as channel:
        logger.info(f"Sending request to {ip}!")
        stub = service_rpc_pb2_grpc.DataSenderStub(channel)
        response = stub.SendImage(service_rpc_pb2.ImageSendRequest(name=name, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response


def send_prediction(data, name, ip, next_request, storage_id, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    with grpc.insecure_channel(ip) as channel:       
        logger.info(f"Sending request to {ip}!")
        stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
        response = stub.StorePrediction(service_rpc_pb2.PredictionStorageRequest(data=data, name=name, storage_id=storage_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_int_to_math_compute(n, next_request, ip, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    with grpc.insecure_channel(ip) as channel:     
        logger.info(f"Sending request to {ip}!")  
        stub = service_rpc_pb2_grpc.MathComputerStub(channel)
        response = stub.ComputeFact(service_rpc_pb2.ComputeFactRequest(n=n, next_request=next_request))

        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_image_to_predictor(encoded_arr, img_width, img_height, client_id, next_request, ip, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    with grpc.insecure_channel(ip) as channel:     
        logger.info(f"Sending request to {ip}!")  
        stub = service_rpc_pb2_grpc.PredictorStub(channel)
        response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=img_width, img_height=img_height, next_request=next_request))
        response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=img_width, img_height=img_height, client_id=client_id, next_request=next_request))
        if response.response_code != 0:
            logger.error(f"ERROR response from {ip}: {response.response_code} - {response.description}")
        else:
            logger.info(f"Received response from {ip}: {response.response_code} - {response.description}")
        return response

def send_output(data, name, ip, next_request, storage_id, logger=None):
    if logger is None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    with grpc.insecure_channel(ip) as channel:       
        stub = service_rpc_pb2_grpc.OutputCollectorStub(channel)
        response = stub.StoreInt(service_rpc_pb2.IntStorageRequest(data=str(data), name=name, storage_id=storage_id, next_request=next_request))
        #TODO LOGGER
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
    
    while start_time - cur_time < TIMEOUT:
        try:
            if node_type == NodeType.MathComputeNode:
                n = args[0]
                return send_int_to_math_compute(n, next_request, ip, logger)
            elif node_type == NodeType.PredictorNode:
                encoded_arr, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
                return send_image_to_predictor(encoded_arr, img_width, img_height, client_id, next_request, ip, logger)
            elif node_type == NodeType.IntSenderNode:
                name, client_id = args[0], args[1]
                return send_request_to_int_sender(name, client_id, next_request, ip)
            elif node_type == NodeType.ImageSenderNode:
                name, img_width, img_height, client_id = args[0], args[1], args[2], args[3]
                return send_request_to_image_sender(name, img_width, img_height, client_id, next_request, ip, logger)
            elif node_type == NodeType.OutputCollectorNode:
                data, name, storage_id = args[0], args[1], args[2]
                return send_output(data, name, ip, next_request, storage_id, logger)
            cur_time = int(round(datetime.datetime.now().timestamp() / 1000))
        except:
            sleep(1)
            logger.info(f"Waiting for response from {node_type}")