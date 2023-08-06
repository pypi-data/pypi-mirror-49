import tensorflow as tf
from tensorflow.python.keras.models import Model
from tensorflow.python.keras import layers
import numpy as np


class NewLayer(Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = layers.Dense(1, activation='sigmoid')

    def call(self, inputs, **kwargs):
        return self.x(inputs)

    def compute_output_shape(self, input_shape):
        output_shape = list(input_shape)
        output_shape[-1] = 1
        return output_shape


ip = layers.Input(shape=(1,))
x = NewLayer()(ip)

model = Model(inputs=ip, outputs=x)
model.summary()

v = tf.zeros([10, 1])
model(v)

optim = tf.keras.optimizers.Adam(0.001)
model.compile(optim, loss='binary_crossentropy', metrics=['acc'])

data = np.linspace(-1., 1., 100).reshape((-1, 1))
labels = np.array([0.] * 50 + [1.] * 50).reshape((-1, 1))

model.fit(data, labels, batch_size=100, epochs=1000)
