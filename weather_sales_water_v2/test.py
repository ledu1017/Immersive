import tensorflow as tf
import tensorflowjs as tfjs

new_model = tf.keras.models.load_model('water.h5')
tfjs.converters.save_keras_model(new_model, './model')