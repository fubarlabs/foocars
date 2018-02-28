#!/usr/bin/python3

import sys, os


import subprocess  
from subprocess import call

remotePath = 'jim@jims-Mac-mini.local:/home/jim/autonomous/data'
localPath = '~/autonomous/data'

command = 'scp -r -i ~/.ssh/id_rsa.pub' + localPath + remotePath, shell=True )

call ( command, shell=True )