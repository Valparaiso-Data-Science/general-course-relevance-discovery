#!/usr/bin/env python3
import os
import sys
import time
from threading import Thread

grobid_ver = "0.6.0"

try:
    os.system("docker -v")
except:
    print("Docker needs to be installed. Exiting...")

'''
try:
    os.system("docker pull lfoppiano/grobid:" + grobid_ver)
except:
    print("Something went wrong. Exiting...")
'''
ans = None

print("Do you want to start grobid now?")
ans = input()

