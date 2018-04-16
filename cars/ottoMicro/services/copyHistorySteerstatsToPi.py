#!/usr/bin/python3

import sys, os

import subprocess
from subprocess import call


#   ---- Generate RSA keys: ----
#   ssh-keygen -t rsa

#   ---- Copy public key to remote machine: ----
#   ssh-copy-id -i [path to rsa file] user@machine


localPathWeights = '/home/jim/Dropbox/foocars/training/weights.h5'
localPathSteerstats = '/home/jim//Dropbox/foocars/training/steerstats.npz'

remotePath = 'pi@jimpi.local:/home/pi/foocars/cars/ottoMicro/data/'

command = 'scp -i ~/.ssh/id_rsa -r ' + localPathWeights + ' ' + remotePath
call ( command, shell=True )

command = 'scp -i ~/.ssh/id_rsa -r ' + localPathSteerstats + ' ' + remotePath
call ( command, shell=True )
