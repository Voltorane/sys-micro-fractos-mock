from concurrent import futures
import logging

import grpc
import cnn_controller_pb2
import cnn_controller_pb2_grpc
import numpy as np
import base64
import sys

sys.path.insert(1, "../Node")
import perceptron

class Predictor(cnn_controller_pb2_grpc.PredictorServicer):
    def Prediction (self, request, context):
        img_arr = np.frombuffer(base64.b64decode(request.image), dtype=np.uint8).reshape(request.img_width, request.img_height, -1)
        b = perceptron.Bot(request.img_width, request.img_height)
        b.data_class_label()
        b.trim_dataset()
        df = b.create_dataframe()
        model = b.train_model(df, df, sample_limit=100, epochs=3)
        label = b.predict_img(model, img_arr)
        # data_class = b.class_labels[int(label)]
        return cnn_controller_pb2.PredictionResponse(label=label)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cnn_controller_pb2_grpc.add_PredictorServicer_to_server(Predictor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()