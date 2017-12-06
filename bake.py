#!/bin/python3 
from time import sleep
import os, argparse

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-i", "--input", help="input file")
args = parser.parse_args()
filein = args.input



os.system("mencoder " + filein + " -o temp.mov -ovc x264")
os.system("ffmpeg -i temp.mov -c:v libx264 baked-" + filein + "")
os.system("del temp.mov")

