#!/usr/bin/python3

import sys, os

import subprocess  
from subprocess import call


#   ---- On pi, Generate RSA keys: ----
#   ssh-keygen -t rsa

#    --- On mac, do this: ----
# In System Preferences / Sharing / Remote Login, change access rights to all users 

#  These needed to be changed too:
# chmod 700 ~/.ssh
# chmod 600 ~/.ssh/authorized_keys

#   ---- From Pi, Copy public key to mac: ----
#   pi@jimPi:~/.ssh $ ssh-copy-id jeo@jims-mac-mini.local

#remotePath = 'jim@jims-Mac-mini.local:/home/jim/autonomous/'
remotePath = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/'

localPath = '/home/pi/autonomous/data/'

#command = 'sudo scp -i ~/.ssh/id_rsa -r /home/pi/autonomous/data/ jim@jim-XPS-13-9360.local:/home/jim/autonomous/'
command = 'sudo scp -i ~/.ssh/id_rsa -r ' + localPath + ' ' + remotePath

call ( command, shell=True )
