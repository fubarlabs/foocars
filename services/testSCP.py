#!/usr/bin/python3

import sys, os

import subprocess  
from subprocess import call


#   ---- Generate RSA keys: ----
#   sudo ssh-keygen -t rsa

#   ---- Copy public key to remote machine: ----
#   sudo ssh-copy-id -i [path to rsa file] user@machine

#remotePath = 'jim@jims-Mac-mini.local:/home/jim/autonomous/'
remotePath = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/'

localPath = '/home/pi/autonomous/data/'

#command = 'sudo scp -i ~/.ssh/id_rsa -r /home/pi/autonomous/data/ jim@jim-XPS-13-9360.local:/home/jim/autonomous/'
command = 'sudo scp -i ~/.ssh/id_rsa -r ' + localPath + ' ' + remotePath

call ( command, shell=True )
