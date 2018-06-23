import numpy as np
import keras 
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten, Reshape
import tensorflow as tf
from history_model import model

model.add(Dense(2+1, activation='linear', kernel_initializer='lecun_uniform'))

datadir='/home/fubar/foocars/cars/motto/curatedData/fubar1/'
imfile='imgs_2018-04-19_20-41-38.npz'
imagedata=np.load(datadir+imfile)['arr_0']

test_im=imagedata[0]
test_im=test_im[20:56, :, :]
model.load_weights('weights_2018-05-03_20-38-32_epoch_28.h5')
prediction=model.predict(np.expand_dims(test_im, axis=0))
print(prediction.shape)
