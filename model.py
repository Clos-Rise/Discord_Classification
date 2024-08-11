import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

np.set_printoptions(suppress=True)


def load_model(model_path, labels_path, image_path):
    model = tf.saved_model.load(model_path)
    class_names = open(labels_path, "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_sus = np.asarray(image)
    normalized_image = (image_sus.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image

    prediction = model(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    score = prediction[0][index].numpy()

    return class_name, score