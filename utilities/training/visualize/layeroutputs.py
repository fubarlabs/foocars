import time
import keras
from keras.layers import Dense
from keras.optimizers import SGD
from keras import backend as K
import numpy as np
#import cv2
import matplotlib.pyplot as plt

from model import model
model.add(Dense(2+1, activation='linear', kernel_initializer='lecun_uniform'))
model.compile(loss=['mse'], optimizer=SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True), metrics=['mse'])

model.load_weights("weights.h5")

layer_dict=dict([(layer.name, layer) for layer in model.layers])

dir_base='/home/fubar/foocars/cars/motto/curatedData/data2/'
filename='imgs_2018-04-06_01-31-28.npz'

sample_images=np.load(dir_base+filename)['arr_0']

model_in=model.input
model_outs=[layer.output for layer in model.layers]
functors=[K.function([model_in]+[K.learning_phase()], [out]) for out in model_outs]

for s in sample_images:
  input_img=np.expand_dims(s[20:56, :, :], axis=0)
  img_result=[func([input_img, 0.]) for func in functors]
  print(len(img_result))
  fig, axes=plt.subplots(2, 2)
  axes[0][0].imshow(np.squeeze(input_img), interpolation='nearest')
  axes[0][1].imshow(img_result[0][0][0][:, :, 11], interpolation='nearest', cmap='Greys')
  axes[1][0].imshow(img_result[0][0][0][:, :, 13], interpolation='nearest', cmap='Greys')
  axes[1][1].imshow(img_result[0][0][0][:, :, 14], interpolation='nearest', cmap='Greys')
  #for i in range(1, 16):
  #  axes[int(i/4)][i%4].imshow(img_result[0][0][0][:, :, i], interpolation='nearest')
  plt.show()
    
    

