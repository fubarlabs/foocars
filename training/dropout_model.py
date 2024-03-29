# The data model converted
import datetime
import os
import glob


import numpy as np
import tensorflow as tf 
from tensorflow.keras import datasets, models, Input 
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import SGD



nrows=36
ncols=128
wr=0.00001 # l1 regularizer value
dp=0.125 # dropout rate 

# Note: Dan used the keras functional paradigm to define his network.
# I'm using the sequential paradigm. 
model= models.Sequential()
frame_in = Input(shape=(3, nrows, ncols), name='img_input')

#we should do a local contrast normalization

print("adding first convolutional layer")
#5x5 convolutional layer with a stride of 2
#model.add(BatchNormalization(input_shape=(nrows, ncols, 3)))
model.add(Conv2D(24, (5, 5), input_shape=(nrows, ncols, 3), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
#model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))
model.add(Dropout(dp))

print("adding second convolutional layer")
#5x5 convolutional layer with a stride of 2
#model.add(BatchNormalization())
model.add(Conv2D(32, (5, 5), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
#model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))
model.add(Dropout(dp))

print("adding third convolutional layer")
#5x5 convolutional layer with a stride of 2
#model.add(BatchNormalization())
model.add(Conv2D(40, (5, 5), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
#model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))
model.add(Dropout(dp))

print("adding fourth convolutional layer")
#3x3 convolutional layer with no stride 
#model.add(BatchNormalization())
model.add(Conv2D(48, (3, 3), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
#model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))
model.add(Dropout(dp))

print("adding fifth convolutional layer")
#3x3 convolutional layer with no stride 
#model.add(BatchNormalization())
model.add(Conv2D(48, (3, 3), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
#model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))
#model.add(BatchNormalization())
model.add(Dropout(dp))


model.add(Flatten())

print("adding fully connected layer")
#fully connected layer
model.add(Dense(100, activation='elu', kernel_initializer='lecun_uniform'))
model.add(Dropout(dp))

print("adding output layer")
#fully connected layer to output node
model.add(Dense(1, activation='linear', kernel_initializer='lecun_uniform'))

model.compile(loss=['mse'], optimizer=SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True), metrics=['mse'])
print(model.summary())
