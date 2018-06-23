import os
import glob
import numpy as np
import matplotlib.pyplot as plt

base_dir="/home/fubar/foocars/cars/motto/curatedData/"
subdirs=["data1", "data2", "data3", "data4", "fubar1"]
directory=base_dir+subdirs[1]
files=glob.glob(os.path.join(directory, 'commands*.npz'))

delay=2

steer_data=np.zeros((0, delay+1))
for f in files:
  command_data=np.load(f)['arr_0']
  steering=command_data[:, 0]
  gt=np.zeros((len(steering)-delay, 0))
  for n in range(0, delay+1):
    delay_data=np.expand_dims(steering[n:len(steering)-(delay-n)], 1)
    gt=np.concatenate((gt, delay_data), axis=1)
  steer_data=np.concatenate((steer_data, gt), axis=0)

binned_steering=np.floor((steer_data-1000)/(1000/9)) 
for i in range(0, binned_steering.shape[0]):
  for j in range(0, binned_steering.shape[1]):
    if binned_steering[i][j]==-1:
      binned_steering[i][j]=0
    elif binned_steering[i][j]==10:
      binned_steering[i][j]=9

count_dict={}

for i in range(0, binned_steering.shape[0]):
  if (binned_steering[i][0], binned_steering[i][1], binned_steering[i][2]) not in count_dict:
    count_dict[(binned_steering[i][0], binned_steering[i][1], binned_steering[i][2])]=1
  else: 
    count_dict[(binned_steering[i][0], binned_steering[i][1], binned_steering[i][2])]+=1

for i in count_dict.keys(): 
  print("("+str(i[0])+","+str(i[1])+","+str(i[2])+")\t"+str(count_dict[i]))
  
print(len(count_dict.keys()))
