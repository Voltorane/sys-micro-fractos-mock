import sys
import os

dir_path = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dir_path,"../Node"))
import math_calc
sys.path.pop(0)

class Adaptor:
    def __init__(self) -> None:
        pass

    # response codes:
    # 0 - success
    # 1 - failure
    # returns  response_code, data, description
    def handle_request(self, req_type, *args):
        if req_type == "COMPUTE_FAC":    
            response_code, result, description = 0, 0, "Factorial successfully calculated!"      
            try:
                n = args[0]
                result = math_calc.factorial(n)
            except Exception as e:
                response_code, description = 1, "Factorial calculation failed!" + str(e)
            return response_code, result, description
        # elif req_type == "COMPUTE_BINOM":
        #     response_code, data, description = 0, 0, "Binom successfully calculated!"      
        #     try:
        #         n, k = args[0], args[1]
        #         data = math_calc.binomial(n, k)
        #     except Exception as e:
        #         response_code, description = 1, "Binom calculation failed!" + str(e)
        #     return response_code, data, description
        