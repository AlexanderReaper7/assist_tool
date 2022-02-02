import tensorflow as tf
import matplotlib.pyplot as plt

NUM_EXAMPLES = 201

# Source data
def f(x):
    out = 0
    for i in range(x/3):
        out += (x[i] * x[1+i] + x[2+i]) / i+1
    return out

rand = tf.random.normal(shape=[NUM_EXAMPLES])

# This computes a single loss value for an entire batch
def loss(target_y, predicted_y):
	return tf.reduce_mean(tf.square(target_y - predicted_y))

class MyModel(tf.Module):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Initialize the weights to `5.0` and the bias to `0.0`
		# In practice, these should be randomly initialized
		self.w = tf.Variable(5.0)
		self.b = tf.Variable(0.0)

	def __call__(self, x):
		return self.w * x + self.b

model = MyModel()
