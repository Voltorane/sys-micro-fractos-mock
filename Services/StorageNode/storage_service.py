from tensorflow.keras.utils import load_img
import numpy as np
import os


def img_to_arr(path, img_width=256, img_height=256):
    if not path.lower().endswith(".jpg"):
        raise ValueError("Error occurred: incorrect path provided.")
    image = load_img(path, target_size=(img_width, img_height))
    img = np.array(image)
    img = img / 255.0
    img = img.reshape(1, img_width, img_height, 3)
    return img

def store_output(path, text):
    response_code, description = 0, "OK"
    try:
        # if not os.path.exists(path):
            # os.makedirs(path)
        with open(path, "w+") as f:
            f.write(text)
    except Exception as e:
        return 1, "FAILURE: " + e.__str__
    else:
        return response_code, description