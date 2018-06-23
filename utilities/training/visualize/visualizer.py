import keras
from keras.layers import Dense
from keras.optimizers import SGD
import numpy as np
#import cv2
import matplotlib.pyplot as plt

from model import model
model.add(Dense(2+1, activation='linear', kernel_initializer='lecun_uniform'))
model.compile(loss=['mse'], optimizer=SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True), metrics=['mse'])


model.load_weights("weights.h5")

layer_dict=dict([(layer.name, layer) for layer in model.layers])

l1filters=layer_dict["conv2d_1"].get_weights()[0]

print(l1filters.shape)

out_image=np.zeros([5*4, 5*6, 3])
print(out_image.shape)

#for n in range(0, 24):
#  cellrow=int(n/6);
#  cellcol=n%6
#  for i in range(0, 5):
#    for j in range(0, 5):
#      for k in range(0, 3):
#        out_image[(cellrow*5+i, cellcol*5+j, k)]=l1filters[(i, j, k, n)]
#fig=plt.imshow(out_image, interpolation="nearest")
#plt.show()
  
#print(out_image)

for i in range(0, 24):
  filt=l1filters[:, :, :, i]
  filt=255*((filt-np.min(filt))/(np.max(filt)-np.min(filt)))
  #newimage=cv2.resize(filt, (0, 0), fx=50, fy=50, interpolation=cv2.INTER_NEAREST)
  #newimage=newimage.astype(int)
  #print(newimage)
  print(filt)
  fig=plt.imshow(filt, interpolation="nearest")
  plt.show()
  #cv2.imshow("l1 filter", newimage)
  #cv2.waitKey(5000)
