# FUBAR Labs Autonomous Racing Vehicles

Autonmous Vehicle Project at Fubar Labs for the Autonomous Powerwheels Racing compeition.
* Autonomous Powerwheels Racing Pittsburg Makerfiare 2017
 * We totally did laps. We were on the track on time and ready to go!
* Autonmous Powerwheels Racing Makerfaire NYC 2017
* Autonmous Vehicle Competition via Sparkfun at Denver Makerfaire 2017

## Quickstart



### Car Code

Prepare your PI

```

```
Get TensorFlow for PI 
```

```
Install Tensorflow for Python 
```
```
Install the Python libraries (poetry):

```
```
Set up the raspberry pi services
```
```

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

### Data Collection Code
Data collection is done as a Raspberry PI service. The folder services contains:

### Training code


## More documentation at the wiki

[Autonomous Project Documenatation](https://github.com/fubarlabs/autonomous/wiki)

## Code details

Simple model in `basic_model.py`.  Currently linear with mean squared error loss (summed over outputs?)

## Inputs

* Webcam image
* Current Accel
* Current Speed

## Outputs

* Steering Wheel angle

# Data sources

