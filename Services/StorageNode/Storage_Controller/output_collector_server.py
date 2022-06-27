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
        id = 0
        with open("client_id.txt", "w+") as f:
            try:
                id = int(f.read())
            except:
                f.write(str(1))
            else:
                if id == "":
                    f.write(str(1))
                else:
                    id += 1
                    f.write(str(id))
        self.adaptor = storage_adaptor.Adaptor(id)
    
    def StoreOutput(self, request, context):
        response_code, description = self.adaptor.handle_request("STORE", request.data, request.name)
        if response_code == 0:
            print("Output storage was successfull!")
        else:
            print(description)
        return service_rpc_pb2.OutputSotrageResponse(response_code=response_code, description=description)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_rpc_pb2_grpc.add_OutputCollectorServicer_to_server(OutputCollector(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()