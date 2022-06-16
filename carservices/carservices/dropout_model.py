# The data model converted
import datetime
import os
import glob


import numpy as np
import tensorflow as tf 
from tensorflow.keras import datasets, models, Input 
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import SGD


class steering_model:

    def __init__(self, nrows, ncols):

        self.nrows=nrows
        self.ncols=ncols
        wr=0.00001 # l1 regularizer value
        dp=0.125 # dropout rate 


        self.model = models.Sequential()
        # speed, accel, distance, angle
        #real_in = Input(shape=(2,), name='real_input')

        #video fram
        frame_in = Input(shape=(3, nrows, ncols), name='img_input')


        print("adding first convolutional layer")
        #5x5 convolutional layer with a stride of 2
        self.model.add(Conv2D(24, (5, 5), input_shape=(nrows, ncols, 3), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
        self.model.add(Dropout(dp))

        print("adding second convolutional layer")
        #5x5 convolutional layer with a stride of 2
        self.model.add(Conv2D(32, (5, 5), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
        self.model.add(Dropout(dp))



        print("adding third convolutional layer")
        #5x5 convolutional layer with a stride of 2
        self.model.add(Conv2D(40, (5, 5), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
        self.model.add(Dropout(dp))

        print("adding fourth convolutional layer")
        #3x3 convolutional layer with no stride 
        self.model.add(Conv2D(48, (3, 3), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
        self.model.add(Dropout(dp))

        print("adding fifth convolutional layer")
        #3x3 convolutional layer with no stride 
        self.model.add(Conv2D(48, (3, 3), strides=(2, 2), activation='elu', padding='same', kernel_initializer='lecun_uniform'))
        self.model.add(Dropout(dp))


        self.model.add(Flatten())

        print("adding fully connected layer")
        #fully connected layer
        self.model.add(Dense(100, activation='elu', kernel_initializer='lecun_uniform'))
        self.model.add(Dropout(dp))

        #M = merge([flat,real_in], mode='concat', concat_axis=1)

        print("adding output layer")
        #fully connected layer to output node
        self.model.add(Dense(1, activation='linear', kernel_initializer='lecun_uniform'))

        self.model.compile(loss=['mse'], optimizer=SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True), metrics=['mse'])
        print(self.model.summary())

    def get_model(self):
        return self.model


    def summary(self):
        print(self.model.summary())
