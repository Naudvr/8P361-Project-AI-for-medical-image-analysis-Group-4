"""
TU/e BME Project Imaging 2021
Simple multiLayer perceptron code for MNIST
Author: Suzanne Wetstein
"""

# disable overly verbose tensorflow logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf


# import required packages
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.callbacks import TensorBoard
#%%

# load the dataset using the builtin Keras method
(X_train, y_train), (X_test, y_test) = mnist.load_data()


# derive a validation set from the training set
# the original training set is split into 
# new training set (90%) and a validation set (10%)
X_train, X_val = train_test_split(X_train, test_size=0.10, random_state=101)
y_train, y_val = train_test_split(y_train, test_size=0.10, random_state=101)



# the shape of the data matrix is NxHxW, where
# N is the number of images,
# H and W are the height and width of the images
# keras expect the data to have shape NxHxWxC, where
# C is the channel dimension
X_train = np.reshape(X_train, (-1,28,28,1)) 
X_val = np.reshape(X_val, (-1,28,28,1))
X_test = np.reshape(X_test, (-1,28,28,1))


# convert the datatype to float32
X_train = X_train.astype('float32')
X_val = X_val.astype('float32')
X_test = X_test.astype('float32')


# normalize our data values to the range [0,1]
X_train /= 255
X_val /= 255
X_test /= 255

# reassign labels
# 0: vertical
# 1: loopy
# 2: curly
# 3: other
y_copy = np.empty(y_train.shape)
y_copy[np.isin(y_train,[1,7])] = 0
y_copy[np.isin(y_train,[0,6,8,9])] = 1
y_copy[np.isin(y_train,[2,5])] = 2
y_copy[np.isin(y_train,[3,4])] = 3
y_train = y_copy

y_copy = np.empty(y_val.shape)
y_copy[np.isin(y_val,[1,7])] = 0
y_copy[np.isin(y_val,[0,6,8,9])] = 1
y_copy[np.isin(y_val,[2,5])] = 2
y_copy[np.isin(y_val,[3,4])] = 3
y_val = y_copy

y_copy = np.empty(y_test.shape)
y_copy[np.isin(y_test,[1,7])] = 0
y_copy[np.isin(y_test,[0,6,8,9])] = 1
y_copy[np.isin(y_test,[2,5])] = 2
y_copy[np.isin(y_test,[3,4])] = 3
y_test = y_copy

# convert 1D class arrays to 4D class matrices
# [1,0,0,0]: vertical
# [0,1,0,0]: loopy
# [0,0,1,0]: curly
# [0,0,0,1]: other
y_train = to_categorical(y_train, 4)
y_val = to_categorical(y_val, 4)
y_test = to_categorical(y_test, 4)

model = Sequential()
# flatten the 28x28x1 pixel input images to a row of pixels (a 1D-array)
model.add(Flatten(input_shape=(28,28,1))) 
# fully connected layer with 64 neurons and ReLU nonlinearity
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
# output layer with 4 nodes (one for each class) and softmax nonlinearity
model.add(Dense(4, activation='softmax')) 


# compile the model
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

# use this variable to name your model
model_name="Four class model"

# create a way to monitor our model in Tensorboard
tensorboard = TensorBoard("logs/" + model_name)

# train the model
model.fit(X_train, y_train, batch_size=32, epochs=10, verbose=1, validation_data=(X_val, y_val), callbacks=[tensorboard])

score = model.evaluate(X_test, y_test, verbose=0)

print("Loss: ",score[0])
print("Accuracy: ",score[1])
