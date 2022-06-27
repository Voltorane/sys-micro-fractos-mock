from tensorflow.keras.utils import load_img
import numpy as np


def img_to_arr(path, img_width=256, img_height=256):
    if not path.lower().endsWith(".jpg"):
        raise ValueError("Error occurred: incorrect path provided.")
    image = load_img(path, target_size=(img_width, img_height))
    img = np.array(image)
    img = img / 255.0
    img = img.reshape(1, img_width, img_height, 3)
    return img
