#!/usr/bin/python3

import sys, os


import subprocess  
from subprocess import call

#remotePath = 'jim@jims-Mac-mini.local:/home/jim/autonomous/'
remotePath = 'jim@jims-XPS-13-9360.local:/home/jim/autonomous/'


localPath = '~/autonomous/data'

command = 'scp -i /home/pi/.ssh/id_rsa -r localPath remotePath

call ( command, shell=True )