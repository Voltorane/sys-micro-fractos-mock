from concurrent import futures
import logging

import grpc
#goto StorageNode
import sys
sys.path.insert(1, "../")
from Storage_Adaptor import storage_adaptor

#goto Services
sys.path.insert(1, "../..")
import service_rpc_pb2_grpc
import service_rpc_pb2

class OutputCollector(service_rpc_pb2_grpc.OutputCollectorServicer):
    def __init__(self) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
    
    def StoreOutput(self, request, context):
        response_code, description = self.adaptor.handle_request("STORE", request.data, request.name, request.storage_id)
        if response_code == 0:
            print("Output storage was successfull!")
        else:
            print(description)
        return service_rpc_pb2.OutputSotrageResponse(response_code=response_code, description=description)

class ImageSender(service_rpc_pb2_grpc.ImageSenderServicer):
    def __init__(self) -> None:
        super().__init__()
        self.adaptor = storage_adaptor.Adaptor()
    
    def send_to_predictor(self, encoded_arr, img_width, img_height, client_id):
        with grpc.insecure_channel('localhost:50051') as channel:       
            stub = service_rpc_pb2_grpc.PredictorStub(channel)
            response = stub.Initialization(service_rpc_pb2.InitRequest(sample_limit=1000, epochs=5, img_width=img_width, img_height=img_height))
            response = stub.Prediction(service_rpc_pb2.PredictionRequest(image=encoded_arr, img_width=img_width, img_height=img_height, client_id=client_id))
            print("Received prediction: " + str(response.data_class))
            return response
    
    def SendImage(self, request, context):
        encoded_arr = self.adaptor.handle_request("SEND", request.name, request.img_width, request.img_height, request.client_id)
        if request.next_node == "PREDICTOR":
            return self.send_to_predictor(encoded_arr, request.img_width, request.img_height, request.client_id)
        return super().SendImage(request, context)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_OutputCollectorServicer_to_server(OutputCollector(), server)
    service_rpc_pb2_grpc.add_ImageSenderServicer_to_server(ImageSender(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()