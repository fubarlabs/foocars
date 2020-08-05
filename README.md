# FUBAR Labs Autonomous Racing Vehicles

Autonmous Vehicle Project at Fubar Labs for the Autonomous Powerwheels Racing compeition.
* Autonomous Powerwheels Racing Pittsburg Makerfiare 2017
 * We totally did laps. We were on the track on time and ready to go!
* Autonmous Powerwheels Racing Makerfaire NYC 2017
* Autonmous Vehicle Competition via Sparkfun at Denver Makerfaire 2017

## Quickstart



### Car Code


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

## Prepare your PI

Obtain the car code by cloning the project
```
git clone https://github.com/fubarlabs/foocars
```

Install system packages
```
sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran python-dev libgfortran5                                   libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev
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

Set up the raspberry pi services
```
cd /etc/systemd/system/
sudo ln -s ~/foocars/cars/carservices/carservices/car.service 
sudo systemctl start car
tail -f /var/log/syslog
```
Verify the car serice is running the car runner


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


