import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import re

IMAGE_DIMENSIONS = (305, 58)

def preproccess_image(image):
    image = np.array(image)
    image = image[:, :, :3]
    image = image.astype(np.float32)
    image = image / 255.0
    return image

images = []
lables = []
# load all images into memory
def load_training_data(sample_count):
    # seach folder for all images
    i = 0 
    for file in Path(Path(__file__).parent.absolute().__str__() + "\\data\\generated_health\\").iterdir():
        print(str(i) + " loading " + file.name)
        # extract lable data from file name
        lable = re.split('h|s|b|x|y|.png',file.name)
        health = int(lable[1])
        shields = int(lable[2])
        # background = int(lable[3])
        # x = int(lable[4])
        # y = int(lable[5])
        img = Image.open(file)
        img = preproccess_image(img)
        images.append(img)
        lables.append((health, shields))
        i += 1
        if i >= sample_count:
            break

load_training_data(1000)

batch_size = 20
dataset = tf.data.Dataset.from_tensor_slices((images, lables))
dataset = dataset.shuffle(1000)
dataset = dataset.batch(batch_size, drop_remainder=True)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(IMAGE_DIMENSIONS[1], IMAGE_DIMENSIONS[0], 3)),
    tf.keras.layers.Dense(IMAGE_DIMENSIONS[0] * IMAGE_DIMENSIONS[1], activation='relu'),
    # tf.keras.layers.Dense(10*8, activation='relu'),
    tf.keras.layers.Dense(2)
])

# def my_loss_fn(y_true, y_pred):
#     squared_difference = tf.square(y_true - y_pred)
#     return tf.reduce_mean(squared_difference, axis=-1)  # Note the `axis=-1`

model.compile(optimizer='adam',
              loss='mae',
              metrics=['accuracy'])

model.fit(dataset, epochs=10)
