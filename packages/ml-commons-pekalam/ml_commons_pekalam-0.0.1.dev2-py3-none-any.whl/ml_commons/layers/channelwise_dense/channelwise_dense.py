import tensorflow as tf
from tensorflow.keras.layers import Dense


class ChannelwiseDense(tf.keras.layers.Layer):

    def __init__(self, input_shape, activation, **kwargs):
        super().__init__(trainable=True, name="channelwise", **kwargs)
        self.input_shape_ = input_shape
        self.layers = []
        for i in range(input_shape[-1]):
            self.layers.append(Dense(input_shape[0] * input_shape[1], activation=activation))

    def build(self, input_shape):
        for l in self.layers:
            l.build((input_shape[0], input_shape[1] * input_shape[2]))
        super().build(input_shape)

    def call(self, inputs, **kwargs):
        out = None
        # reshape to (batch, x * y, f)
        x = tf.reshape(inputs, tf.constant([-1, inputs.shape[1] * inputs.shape[2], inputs.shape[3]], dtype=tf.int32))
        for i in range(len(self.layers)):
            # reshape to (batch, x, y, 1)
            d_out = tf.reshape(self.layers[i](x[:, :, i]),
                               tf.constant([-1, inputs.shape[1], inputs.shape[2]], dtype=tf.int32))
            d_out = tf.expand_dims(d_out, -1)
            if out is not None:
                out = tf.concat([d_out, out], axis=-1)
            else:
                out = d_out
        return out
