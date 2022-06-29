from tensorflow.keras.utils import load_img
import numpy as np
import os
import shutil
import base64

dir_path = os.path.dirname(__file__)

def img_to_arr(name, img_width, img_height, client_id, storage_dir):
    if not name.lower().endswith(".jpg"):
        raise ValueError("Error occurred: incorrect name provided.")
    path_to_image = os.path.join(dir_path, storage_dir, client_id, name)
    image = load_img(path_to_image, target_size=(img_width, img_height))
    img = np.array(image)
    img = img / 255.0
    img = img.reshape(1, img_width, img_height, 3)
    return base64.b64encode(img)

def store_data(name, storage_dir, data, storage_id=""):
    # common storage for all unordered requests
    if storage_id == "":
        storage_id="common"
    storage_path = os.path.join(dir_path, storage_dir, storage_id)
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    response_code, description = 0, "OK"
    if name == "" or name is None:
        name = "output"
    path_to_file = os.path.join(storage_path, name)
    try:
        with open(path_to_file, "w+") as f:
            f.write(str(data))
    except Exception as e:
        return 1, "FAILURE: " + str(e)
    else:
        return response_code, description


def read_int(name, client_id, storage_dir):
    path_to_file = os.path.join(dir_path, storage_dir, client_id, name)
    with open(path_to_file, "r") as f:
        n = f.read()
        return int(n)

if __name__ == "__main__":
    # store_data("test", "storage", 1, "admin")
    pass