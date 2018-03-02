#!/usr/bin/python3

import sys, os


import subprocess  
from subprocess import call

#remotePath = 'jim@jims-Mac-mini.local:/home/jim/autonomous/'
remotePath = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/'


localPath = '/home/pi/autonomous/data/'

command = 'scp -i ~/.ssh/id_rsa -r ' + localPath + ' ' + remotePath

#command = 'sudo scp -i ~/.ssh/id_rsa -r /home/pi/autonomous/data/ jim@jim-XPS-13-9360.local:/home/jim/autonomous/'


call ( command, shell=True )
