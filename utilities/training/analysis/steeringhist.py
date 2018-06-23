import os
import glob
import numpy as np
import matplotlib.pyplot as plt

base_dir="/home/fubar/foocars/cars/motto/curatedData/"
subdirs=["data1", "data2", "data3", "data4", "fubar1"]

filelist={}

for i in subdirs:
  filelist[i]=glob.glob(os.path.join(base_dir+i, 'commands*.npz'))

steerstats={}
speedstats={}
for i in subdirs:
  steerstats[i]=np.array([])
  speedstats[i]=np.array([])
  for j in filelist[i]:
    commdata=np.load(j)['arr_0']
    steerstats[i]=np.concatenate((steerstats[i], commdata[:, 0]), axis=0)
    speedstats[i]=np.concatenate((speedstats[i], commdata[:, 1]), axis=0)
  #plt.hist(steerstats[i], bins=11)
  #plt.title(i)
  #plt.show()

steerdata=np.array([])
for i in steerstats.keys():
  steerdata=np.concatenate((steerdata, steerstats[i]), axis=0)
  
plt.hist(steerdata, bins=9, range=(1000, 2000))
plt.title("all data")
plt.show()
  
