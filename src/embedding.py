import cv2
import numpy as np
import os
import glob

from tensorflow.keras.models import load_model

import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras.utils import CustomObjectScope

with CustomObjectScope({'tf': tf}):
    model = load_model('./model/nn4.small2.lrn.h5')
    # , compile=False)

#model = load_model('./model/facenet_keras.h5')
def image_to_embedding(image, model):
    image = cv2.resize(image, (96, 96))  # use 96, 96 for small2.lrn
    img = image[..., ::-1]
    img = np.around(np.transpose(img, (0, 1, 2)) / 255.0, decimals=12)
    x_train = np.array([img])
    embedding = model.predict_on_batch(x_train)
    return embedding


def create_embeddings():
    input_embeddings = {}

    for file in glob.glob("./data/datasets/*"):
        person_name = os.path.splitext(os.path.basename(file))[0]
        image_file = cv2.imread(file, 1)
        input_embeddings[person_name] = image_to_embedding(image_file, model)

    return input_embeddings