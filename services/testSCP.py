#!/usr/bin/python3

import sys, os

import subprocess  
from subprocess import call


#   ---- Generate RSA keys: ----
#   ssh-keygen -t rsa

#   ---- Copy public key to remote machine: ----
#   ssh-copy-id -i [path to rsa file] user@machine

# I found the culprit. In System Preferences / Sharing / Remote Login, the access rights were checked for Administrator only. 
# After I changed to Everyone, to worked like it used to.

#remotePath = 'jim@jims-Mac-mini.local:/home/jim/autonomous/'
remotePath = 'jim@jim-XPS-13-9360.local:/home/jim/autonomous/'

localPath = '/home/pi/autonomous/data/'

#command = 'sudo scp -i ~/.ssh/id_rsa -r /home/pi/autonomous/data/ jim@jim-XPS-13-9360.local:/home/jim/autonomous/'
command = 'sudo scp -i ~/.ssh/id_rsa -r ' + localPath + ' ' + remotePath

call ( command, shell=True )
