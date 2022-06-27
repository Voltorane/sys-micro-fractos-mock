from tensorflow.keras.utils import load_img
import numpy as np
import os
import base64


def img_to_arr(path, img_width=256, img_height=256):
    if not path.lower().endswith(".jpg"):
        raise ValueError("Error occurred: incorrect path provided.")
    image = load_img(path, target_size=(img_width, img_height))
    img = np.array(image)
    img = img / 255.0
    img = img.reshape(1, img_width, img_height, 3)
    return base64.b64encode(img)

def store_output(name, storage_dir, data):
    response_code, description = 0, "OK"
    if name == "" or name is None:
        name = "output"
    try:
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        with open(os.path.join(storage_dir, name), "w+") as f:
            f.write(data)
    except Exception as e:
        return 1, "FAILURE: " + str(e)
    else:
        return response_code, description