#FOOCAR SCHEMA


## Table of Contents
1. [Car Modes](#modes)

2. [Car Architecture](#architecture)

3. [Where Can I Learn More?](#biblio)

## Car Modes <a name="modes"></a>
The car can be setup to perform three different tasks. The type of task to be performed is controlled by onboard switches.

**1. Data Collection Mode**
In this mode, the car acts as a recording device. To record the variables of interest, the car is run several times on the racing circuit using a remote controller. 

The recorded variables are:

* video images
* steering angle 
* throttle intensity 
* time tracking 

The video images are recorded using the car's PI embedded camera and stored on the mini computer attached to the car. The mini computer is usually a Raspberry PI or an NVIDIA board.

The steering angle and speed are directly read from the signal sent by the remote controller.
  

**2. Autonomous Driving Mode**
The environment data gathered under the "Data Collection Mode" is passed to an external GPU to calibrate the car's driving model.

The autonomous driving model is based on a Machine Learning model called Convolutional Neuronal Network (CNN). The paper [1] referenced in the Bibliography section expands on the calibration of the driving model.

After the model parameters are calibrated, they are uploaded to the car's CNN model stored on the mini computer. While driving, the images collected by the camera will be passed to the mini computer's model to the car's speed and steering.


**3. Data Collection in Autonomous Mode**
This mode is a combination of the two above. The car is able to record the steering angles and camera images while driving in autonomous mode. 


## Car Architecture <a name="architecture"></a>
 Similar to a human driving, the car's camera would be the human eyes and the mini-computer would be the brain. The camera records the environment and passes the images to the car's mini-computer. The mini-computer takes the images and pass them to the calibrated CNN driving algorithm. The model outputs are the car speed and steering direction. These two outputs are sent to the Arduinos controlling the motor and servo.
 
Below we show a diagram of the Fuvette's architecture. 




## Bibliography <a name="biblio"></a>
1. *End to End Learning for Self Driving Cars*
   
        https://arxiv.org/abs/1604.07316

2.FUBAR Lab's Github page:

     https://github.com/fubarlabs/foocars