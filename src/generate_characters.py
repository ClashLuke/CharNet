import numpy as np
import tensorflow as tf


class GeneratorCallback(tf.keras.callbacks.Callback):
    """
    Keras callback to generate and print a string using the previously trained model
    when the epoch ends.
    """

    def __init__(self, input_string, inputs, output_characters, dtype):
        self.input_string = tf.convert_to_tensor(np.array([ord(input_string[i])
                                                           for i in range(inputs)],
                                                          dtype=np.int32))
        self.inputs = inputs
        self.output_characters = output_characters
        super().__init__()

    @tf.function(experimental_relax_shapes=True)
    def _generate_string(self):
        inp = tf.identity(self.input_string)
        model = self.model
        with tf.compat.v1.Session() as sess:
            for i in range(self.output_characters):
                inp = tf.concat([inp,
                                tf.cast(tf.math.argmax(
                                        model.predict_on_batch((tf.reshape(inp[i:],
                                                                           (1, -1))))[
                                            0]),
                                        tf.int32)],
                                0)
            out = ''.join(map(chr, inp[self.inputs:].eval(session=sess)))
        return out

    def on_epoch_end(self, epoch, logs=None):
        """
        Function called when a training epoch ends. Generates and prints a string.
        :param epoch: Index of the current epoch, ignored
        :param logs: Logs generated during training, ignores
        :return: None
        """
        print(self._generate_string())
