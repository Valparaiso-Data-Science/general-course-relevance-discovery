#!/usr/bin/env python3
import os
import sys
import time

try:
    os.system("git --version")
except:
    print("Git needs to be installed. Exiting...")
    sys.exit()

try:
    os.system("git clone https://github.com/kermitt2/grobid-client-python")
except:
    print("Something went wrong in the cloning process. Exiting...")
    sys.exit()



