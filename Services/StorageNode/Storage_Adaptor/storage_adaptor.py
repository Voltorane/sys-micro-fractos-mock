import sys
import os

sys.path.insert(1, "../Node")
import storage_service

class Adaptor:
    def __init__(self) -> None:
        self.STORAGE_PATH = "../Node/storage/"
        self.TARGET_PATH = "../Node/target/"
    
    # response codes:
    # 0 - success
    # 1 - failure
    # returns  response_code, label, data_class
    def handle_request(self, req_type, *args):
        if req_type == "STORE":
            data, name, storage_id = args
            response_code, description = storage_service.store_output(name, self.TARGET_PATH, data, storage_id)
            return response_code, description
        elif req_type == "SEND":
            name, img_width, img_height, client_id = args
            encoded_image = storage_service.img_to_arr(name, img_width, img_height, client_id, self.STORAGE_PATH)
            return encoded_image
        elif req_type == "RESET":
            pass
        