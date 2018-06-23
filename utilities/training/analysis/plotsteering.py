import os 
import glob
import argparse
import numpy as np
import matplotlib.pyplot as plt

base_dir="/home/fubar/foocars/cars/motto/curatedData/"

subdirs=["data1", "data2", "data3", "data4", "fubar1"]

directory=base_dir+subdirs[4]
print(directory)

files=glob.glob(os.path.join(directory, 'commands*.npz'))
print(files)

for f in files:
  command_data=np.load(f)['arr_0']
  steering=command_data[:, 0]
  print(len(steering))
  t=np.arange(0, len(steering))
  fig, ax=plt.subplots()
  ax.plot(t, steering)
  print(ax)
  plt.show()
