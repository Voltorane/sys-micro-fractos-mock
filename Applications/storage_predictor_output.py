from __future__ import print_function
import logging
import grpc
import sys
sys.path.insert(1, "../Services")
import service_rpc_pb2
import service_rpc_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:       
        stub = service_rpc_pb2_grpc.ImageSenderStub(channel)
        name = "1.jpg"
        client_id = "TEST"
        img_width = 128
        img_height = 128
        next_node = "PREDICTOR"
        output_name = "test_name"
        next_request = [f"PREDICTOR,127.0.0.1:50051,img_width:{img_width},img_height:{img_height},client_id:{client_id}",
                        f"STORAGE,127.0.0.1:50052,name:{output_name},storage_id:{client_id}"]
        response = stub.SendImage(service_rpc_pb2.ImageSendRequest(name=name, img_width=img_width, img_height=img_height, client_id=client_id, next_node=next_node, next_request=next_request))
        # encoded_arr = storage_service.img_to_arr('storage/0.jpg', 128, 128)
        # response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=128, img_height=128))
        # response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=128, img_height=128))
        print("Received response: " + str(response))

if __name__ == '__main__':
    logging.basicConfig()
    run()