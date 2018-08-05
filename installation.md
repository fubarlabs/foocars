Quick Installation
====

Prepare your Raspberry PI (Stretch)
```
apt-get update 

apt-get install  apt-utils wget unzip build-essential cmake pkg-config \
  libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev \
  libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
  libxvidcore-dev libx264-dev \
  libgtk2.0-dev libgtk-3-dev \
  libatlas-base-dev gfortran \
  python3-dev python3-pip python-pip python3-h5py \
  python3-numpy python3-matplotlib python3-scipy python3-pandas libatlas-base-dev
```

Install the Pythonn Environment Management Tool: pipenv

```
pip3 install pipenv
```


# Enable command line Arduino via platformio
```
 pip install platformio
```

# Enable pic32 compiler execution
```
ln -s /lib/arm-linux-gnueabihf/ld-linux.so.3 /lib/ld-linux.so.3
pio platform install microchippic32
pio platform install teensy
```

# Test if pio is working
```
pio device list 
```

#Python Dependencies

Make sure you are in the foocars directory. All the Python environment dependencies are in the Pipfile.

pipenv install

#Activate the python environment
```
pipenv shell
```

# Enable CarRunner service

# Set up the raspberry pi services
```
ln -s /foocars/cars/carRunner.py
systemctl enable carRunner.service
```
