import sys
import base64
import numpy as np

sys.path.insert(1, "../Node")
import perceptron

class Adaptor:
    def __init__(self) -> None:
        self.DEFAULT_EPOCHS = 3
        self.DEFAULT_SAMPLE_LIMIT = 1000
    
    # def prepare_labels(self, bot):
    #     bot.data_class_label()
    #     bot.trim_dataset()
    
    # def train(self, bot, sample_limit, epochs, img_width, img_height):
    #     df = bot.create_dataframe()
    #     return bot.train_model(df, df, sample_limit=sample_limit, epochs=epochs)
    
    # response codes:
    # 0 - success
    # 1 - failure
    # returns  response_code, label, data_class
    def handle_request(self, req_type, *args):
        if req_type == "INIT":
            # MOCK
            return 0, "OK"
            
            try:
                sample_limit, epochs, img_width, img_height = args
                
                # model not provided (needs training)
                b = perceptron.Bot(img_width, img_height)
                # self.prepare_labels(b)
                if not b.has_models():
                    b.train(b.df, b.df, sample_limit=sample_limit, epochs=epochs)
                # response_code, description
                return 0, "OK"
            except Exception as e:
                print(e.with_traceback())
                # response_code, description
                return 1, str(e)
        elif req_type == "PREDICT":
            #MOCK 
            return 0, 1, "Cat", "OK"
            
            try:
                encoded_image, img_width, img_height = args
                img_arr = np.frombuffer(base64.b64decode(encoded_image), dtype=np.float64).reshape(1, img_width, img_height, 3)
                b = perceptron.Bot(img_width, img_height)
                if not b.has_models():
                    # model = self.train(b, self.DEFAULT_SAMPLE_LIMIT, self.DEFAULT_EPOCHS, img_width, img_height)
                    model = b.train(b.df, b.df, sample_limit=self.DEFAULT_SAMPLE_LIMIT, epochs=self.DEFAULT_EPOCHS)
                    # b.data_class_label()
                    # b.trim_dataset()
                    # df = b.create_dataframe()
                    # model = b.train_model(df, df, sample_limit=100, epochs=3)
                model = b.load_model()
                label = b.predict_img(model, img_arr)
                data_class = b.label_list[int(label)]
                # response_code, label, data_class, description
                return 0, label, data_class, "OK"
            except Exception as e:
                print(e)
                # return 1, None, None
                # response_code, label, data_class, description
                return 1, None, None, str(e)
        