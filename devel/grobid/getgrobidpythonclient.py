#!/usr/bin/env python3
import os
import sys
import time

# directory name for grobid python client
dirname = 'grobid-client-python'
if sys.argv[1] is not None:
    dirname = sys.argv[1]

try:
    os.mkdir(dirname)
except:
    print("Directory already exists!")

os.chdir(dirname)
os.system("git clone https://github.com/kermitt2/grobid-client-python")



