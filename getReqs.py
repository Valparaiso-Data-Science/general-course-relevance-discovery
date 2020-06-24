#!/usr/bin/env python3
import os
from sys import platform
os.system("pip install -r requirements.txt")
os.system("python -m spacy download en")
if platform == "linux":
    print("--------------------------------------------------------------------------")
    print("Use your package manager to install 'enchant'")
    print("--------------------------------------------------------------------------")
elif platform == "darwin":
    os.system("brew install enchant")
elif platform == "win32":
    print("--------------------------------------------------------------------------")
    print("You need to install 'enchant' for the wordninja parsing to work correctly")
    print("--------------------------------------------------------------------------")
