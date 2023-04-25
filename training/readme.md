# Project Title: Autonomous Vehicle Steering Prediction

## Description
This project aims to create a deep learning model for predicting steering angles in an autonomous vehicle using images as input. The code implements a Convolutional Neural Network (CNN) using the Keras library and trains the network with image and steering angle data.

## Dependencies
- Python 3.x
- numpy
- os
- glob
- datetime
- argparse
- tensorflow
- keras

## Installation

Install Python version 3.9

Install poetry
`pip install poetry`

Make sure you're in the training directory:
`cd training`

Install the software
`poetry install`

Run the train.py to make sure it's functioning

`poetry run python train.py`

Get training Data
`curl -LO https://drive.google.com/file/d/1SYe2EXlY9GA5x_voak5IrxmZVCDaP9xJ/view?usp=share_link`

Decompress the training data
`tar xvzf collected.tar.gz`

Run training with default settings on the directory to the files:
`poetry run python train.py c:\downloads\collected`


## Getting Started
1. Ensure that you have installed all the necessary dependencies.
2. Collect and store training data (images and corresponding steering angles) in one or more directories.
3. Adjust any necessary parameters in the `defines.py` file, such as image size and cropping settings.
4. Run the script using the command line, specifying any desired arguments (see below for details).

## Usage
python <script_name>.py [--weight_filename WEIGHT_FILENAME] [--init_weights INIT_WEIGHTS] [--delay DELAY] [--epochs EPOCHS] [--save_frequency SAVE_FREQUENCY] directories [directories ...]


### Arguments
- `--weight_filename`: Prefix for saved weight files (default: 'weights').
- `--init_weights`: Specifies an existing weight file to use as an initial condition for the network at the start of training (default: '').
- `--delay`: Delay between image and steering training data to compensate for processing delay during runtime (default: 0).
- `--epochs`: Number of epochs to train over (default: 100).
- `--save_frequency`: Number of epochs between weight file saves (default: 10).
- `directories`: List of directories to read training data from.

## Outputs
The script will save the following files during and after training:
1. Weight files: Saved every `--save_frequency` epochs and once training is complete. The filenames follow the format `WEIGHT_FILENAME_TIMESTAMP_epoch_EPOCH.h5`.
2. `steerstats.npz`: File containing steering angle mean and standard deviation for future use.
3. `training_hist.png`: A plot of the training history, showing validation loss over epochs.



