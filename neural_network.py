# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import model_from_json

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
import pandas as pd

def give_me_model():

    print(tf.__version__)

    data = pd.read_csv('data.csv')

    train_images = data.iloc[:, 0:4]
    train_labels = data.iloc[:, 4]

    #model = keras.Sequential([
        #keras.layers.Flatten(input_shape=((784))),
        #keras.layers.Dense(128, activation=tf.nn.relu),
        #keras.layers.Dense(10, activation=tf.nn.softmax)
    #])

    model = keras.Sequential()
    model.add(keras.layers.Dense(100, input_shape = (4, ), activation=tf.nn.relu));
    model.add(keras.layers.Dense(100, activation=tf.nn.relu));
    model.add(keras.layers.Dense(100, activation=tf.nn.relu));
    model.add(keras.layers.Dense(100, activation=tf.nn.relu));
    model.add(keras.layers.Dense(100, activation=tf.nn.relu));
    model.add(keras.layers.Dense(4, activation=tf.nn.softmax));

    model.compile(optimizer=tf.train.AdamOptimizer(), 
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    X = np.array(train_images.values.tolist())
    Y = np.array(train_labels.values.tolist())

    model.fit(X, Y, epochs = 50, verbose=2)

    model.save('game_model.h5')

    return model

    #predictions = model.predict(test_images)

    #print(sum(np.equal(np.argmax(predictions, axis = 1), test_labels)) / np.size(test_labels))

if __name__ == "__main__":
    give_me_model()
