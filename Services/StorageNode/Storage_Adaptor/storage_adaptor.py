import sys
import os

sys.path.insert(1, "../Node")
import storage_service

class Adaptor:
    def __init__(self, client_id) -> None:
        self.STORAGE_PATH = "../Node/storage_" + str(client_id)
        self.TARGET_PATH = "../Node/target_" + str(client_id)
    
    # response codes:
    # 0 - success
    # 1 - failure
    # returns  response_code, label, data_class
    def handle_request(self, req_type, *args):
        if req_type == "STORE":
            data, name = args
            response_code, description = storage_service.store_output(name, self.TARGET_PATH, data)
            return response_code, description
        elif req_type == "SEND":
            name = args
            
            pass
        elif req_type == "RESET":
            pass
        