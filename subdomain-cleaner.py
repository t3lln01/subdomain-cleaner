#!/usr/bin/python3

import os
import sys
import subprocess
import string
import random

bashfile=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile='/tmp/'+bashfile+'.sh'

f = open(bashfile, 'w')
s = """#!/usr/bin/env bash

awk -F"." '{ k[$(NF-1)"."$(NF)]++}END{for (i in k){print i}}' $1 | grep -v '\.(com|co|org|gov)\.[a-z]{2}' | sed 's/\./[.]/g'
"""
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd=bashfile
for arg in sys.argv[1:]:
  bashcmd += ' '+arg
subprocess.call(bashcmd, shell=True)
