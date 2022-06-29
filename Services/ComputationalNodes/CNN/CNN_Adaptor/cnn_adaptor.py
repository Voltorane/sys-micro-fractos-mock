import sys
import base64
from urllib import response
import numpy as np

sys.path.insert(1, "../Node")
import perceptron

class Adaptor:
    def __init__(self) -> None:
        self.DEFAULT_EPOCHS = 3
        self.DEFAULT_SAMPLE_LIMIT = 1000

    # response codes:
    # 0 - success
    # 1 - failure
    # returns  response_code, label, data_class
    def handle_request(self, req_type, *args):
        if req_type == "INIT":    
            response_code, description = 0, "Model successfully initialized!"      
            try:
                sample_limit, epochs, img_width, img_height = args
                b = perceptron.Bot(img_width, img_height)
                if not b.has_models():
                    b.train_model(b.df, b.df, sample_limit=sample_limit, epochs=epochs)
            except Exception as e:
                print(e)
                response_code, description = 1, "Model initialization failed!" + str(e)
            return response_code, description
        elif req_type == "PREDICT":
            response_code, label, data_class, description = 0, None, None, "Prediction successed!"
            try:
                encoded_image, img_width, img_height = args
                img_arr = np.frombuffer(base64.b64decode(encoded_image), dtype=np.float64).reshape(1, img_width, img_height, 3)
                b = perceptron.Bot(img_width, img_height)
                if not b.has_models():
                    model = b.train_model(b.df, b.df, sample_limit=self.DEFAULT_SAMPLE_LIMIT, epochs=self.DEFAULT_EPOCHS)
                model = b.load_model()
                try:
                    label = b.predict_img(model, img_arr)
                except Exception as e:
                    print(str(e))
                    model = b.train_model(b.df, b.df, sample_limit=self.DEFAULT_SAMPLE_LIMIT, epochs=self.DEFAULT_EPOCHS)
                    label = b.predict_img(model, img_arr)
                data_class = b.label_list[int(label)]
            except Exception as e:
                response_code, description = 1, "Prediction failed!" + str(e)
            return response_code, label, data_class, description
        