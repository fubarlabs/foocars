# What is FOO Cars?

This autonomous vehicle project's goal is to create autonomous racing vehicles in the simplest possible way—a good first car.  The name is a mash-up of Fubar Labs, the mysterious planes called "foo fighters" and "foobar" the ubiquitous getting started variables for programming.  The control system can scale to any vehicles using RC controls.

## How has this project been used?
* CHI@Edge 2021 Summer Internship
  * Virtualize the deployment of vehicle and code on the edge of super computer envrionment.

### FUBAR Labs Autonomous Racing Vehicles

Autonmous Vehicle Project at Fubar Labs for the Autonomous Powerwheels Racing compeition.
* Bergen Technical Highschool Workshop Spring 2023
* Bergen Technical Highschool Workshop Spring 2021
* Autonomous Powerwheels Racing Pittsburg Makerfiare 2017
 * We totally did laps. We were on the track on time and ready to go!
* Autonmous Powerwheels Racing Makerfaire NYC 2017
* Autonmous Vehicle Competition via Sparkfun at Denver Makerfaire 2017

## Quickstart


### Car Code

## Prepare your PI

Obtain the car code by cloning the project
```
git clone https://github.com/fubarlabs/foocars
```

For the Tensorflow 1.15 version fetch the wheel file to the local system:
```
cd ~/foocars
sh get_tensorflow.sh
```


Install system packages
```
sudo apt-get  install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

```

Install poetry
```
sudo pip3 install poetry
```

Install platformio
```
sudo pip3 install platformio
```

Use poetry to create the generate the car
```
cd ~/foocars/cargenerator
poetry install
poety run generatecar --name yourhostname --output_dir /home/pi/foocars/cars/
```

Use poetry to create the car code and service
```
cd ~/foocars/cars/carservices
poetry install
```

Test the PI Hat
```
poetry run test_pihat
```

Test the Car Runner
```
poetry run car_runner
```

Verify the leds and switches are working.



## Pepare the RC Car and Arduino

### Note for Arduino
Code is installed from the Raspberry PI using PLatform IO
```
sudo pip3 install platformio

```

### Teensy 3.2 Code

```
cd ./cars/templatecar/arduino/teensy-FullAutoDrive-port
```


### Arduino Code

```
pio run -t upload
```


### Finish the PI set up
Set up the raspberry pi services
```
cd /etc/systemd/system/
sudo ln -s ~/foocars/cars/carservices/carservices/car.service 
sudo systemctl start car
tail -f /var/log/syslog
```
Verify the car service is running the car runner


## Training code

Find a system with a good gpu. It was slow but worked on a Raspberry PI 4.
```
cd ~/foocars/training

poetry install
poetry shell
```
The training command:
```
Using TensorFlow backend.
usage: train.py [-h] [--weight_filename WEIGHT_FILENAME]
                [--init_weights INIT_WEIGHTS] [--delay DELAY]
                [--epochs EPOCHS] [--save_frequency SAVE_FREQUENCY]
                directories [directories ...]
```
Run the training:
```
python train.py --epochs 100 --save_frequency 2 ../cars/youcar/data/collected
```

### Alternately use this example Google Colab Notebook
* FooCars Training: https://colab.research.google.com/drive/1LxZyNQvWT2VasnOrNkU9dTcpo4B9I0aD?usp=sharing


### 2023 Training with Docker

https://colab.research.google.com/drive/1oT3M4QVUoNYkFh4pzktVNBfT0zULwSpM?usp=sharing
