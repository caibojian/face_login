import tensorflow as tf
from tensorflow import keras
import numpy as np
import face_recognition
import data

def train_face():
    train_x, train_y, test_x, test_y = data.generateds()
    dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
    dataset = dataset.batch(32)
    dataset = dataset.repeat()
    OUTPUT_NODE, TRAIN_DATA_SIZE, TEST_DATA_SIZE = data.get_out_put_node()
    model = keras.Sequential([
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(OUTPUT_NODE, activation=tf.nn.softmax)
    ])

    model.compile(optimizer=tf.train.AdamOptimizer(),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    steps_per_epoch  = 30
    if steps_per_epoch > len(train_x):
        steps_per_epoch = len(train_x)
    model.fit(dataset, epochs=10, steps_per_epoch=steps_per_epoch)

    model.save('model/face_model.h5')
def main():
    train_face()
    
if __name__ == '__main__':
    main()

