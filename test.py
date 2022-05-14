from tensorflow.keras.models import load_model

import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras.utils import CustomObjectScope

with CustomObjectScope({'tf': tf}):
    model = load_model('./model/trained_model.h5')
print(model.summary())