#!/usr/bin/env python3
import os
import sys
import time

try:
    os.system("git --version")
except:
    print("Git needs to be installed. Exiting...")
    sys.exit()


if len(sys.argv) < 2:
    print("You need to provide an output directory!!")
    sys.exit()


try:
    try:
        os.mkdir(sys.argv[1])
    except:
        print("Directory already exists!")
    os.chdir(sys.argv[1])
    os.system("git clone https://github.com/kermitt2/grobid-client-python")
except:
    print("Something went wrong in the cloning process. Exiting...")
    sys.exit()



