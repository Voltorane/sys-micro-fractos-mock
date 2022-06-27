from concurrent import futures
import logging

import grpc
import cnn_controller_pb2
import cnn_controller_pb2_grpc
import storage_service

class OutputCollector(cnn_controller_pb2_grpc.OutputCollectorServicer):
    def StoreOutput(self, request, context):
        response_code, description = storage_service.store_output("target/output", request.text)
        return cnn_controller_pb2.OutputSotrageResponse(response_code=response_code, description=description)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cnn_controller_pb2_grpc.add_OutputCollectorServicer_to_server(OutputCollector(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()