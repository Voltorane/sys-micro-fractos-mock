import sys
import os

dir_path = os.path.dirname(__file__)

sys.path.insert(1, os.path.join(dir_path,"../Node"))
import storage_service
sys.path.pop(0)

config_dir = os.path.join(dir_path,"../../config")

class Adaptor:
    def __init__(self) -> None:
        # self.STORAGE_PATH = "../Node/storage/"
        self.STORAGE_PATH = "../../storage/"
        with open(os.path.join(config_dir, "storage_path"), "r") as storage_path_config:
            self.STORAGE_PATH = storage_path_config.read()
        self.TARGET_PATH = "../Node/target/"
    
    # response codes:
    # 0 - success
    # 1 - failure
    # returns  response_code, label, data_class
    def handle_request(self, req_type, *args):
        if req_type == "STORE":
            data, name, storage_id = args
            response_code, description = 0, "Output successfully stored!"
            try:
                storage_service.store_data(name, self.STORAGE_PATH, data, storage_id)
            except Exception as e:
                response_code, description = 1, "Failed to store output: " + str(e)
            return response_code, description
        elif req_type == "SEND_IMAGE":
            name, img_width, img_height, client_id = args
            response_code, description = 0, "Image encoded sucessfully!"
            try:
                encoded_image = storage_service.img_to_arr(name, img_width, img_height, client_id, self.STORAGE_PATH)
            except Exception as e:
                response_code, encoded_image, description = 1, None, "Image encoding failed: " + str(e)
            return response_code, encoded_image, description
        elif req_type == "SEND_INT":
            name, client_id = args
            response_code, description = 0, "Integer retrieved sucessfully!"
            try:
                num = storage_service.read_int(name, client_id, self.STORAGE_PATH)
            except Exception as e:
                response_code, num, description = 1, None, "Integer retrieving failed: " + str(e)
            return response_code, num, description
        elif req_type == "RESET":
            pass
        