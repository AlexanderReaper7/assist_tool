import numpy as np
import tensorflow as tf
from sklearn.datasets import make_classification

data = make_classification(n_samples=1000, n_features=305, n_classes=3, n_clusters_per_class=1)
inputs = data[0]
tragets = data[1]

def change_shape(inputs, labels): # In your case you will load the image here
    first = inputs[0]
    first = tf.reshape(first, (10,10,3))
    return ((first, inputs[1]), labels)

dataset = tf.data.Dataset.from_tensor_slices(((inputs[:, :300], inputs[:, 300:]), data[1]))
dataset = dataset.map(change_shape)
dataset = dataset.batch(20)

inputa = tf.keras.layers.Input(shape = (10,10,3))
inputb = tf.keras.layers.Input(shape = (5))
conva = tf.keras.layers.Conv2D(15, 3, activation='relu')(inputa)
layera = tf.keras.layers.Flatten()(conva)
layerb = tf.keras.layers.Dense(15, activation='relu')(inputb)
concat = tf.keras.layers.Concatenate()([layera, layerb])
out = tf.keras.layers.Dense(3, activation='softmax')(concat)

model = tf.keras.models.Model(inputs=[inputa, inputb], outputs=[out])

model.compile(
              loss=tf.keras.losses.SparseCategoricalCrossentropy(), #or categorical_crossentropy
              optimizer='adam',
              metrics = ['accuracy']
              )

model.fit(dataset, epochs=2)