#!/bin/python2.7

import argparse
import re
import random
import struct
from itertools import chain

#################
### ARGUMENTS ###
#################

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("file", help="input file")
parser.add_argument("-o", "--output", help="output file")
parser.add_argument('-m', "--mode", action='store', dest='modevalue',help='choose mode')
parser.add_argument('-c', action='store', dest='countframes',help='var1', default=1)
parser.add_argument('-n', action='store', dest='positframes',help='var2', default=1)
parser.add_argument('-s', action='store', dest='simple_value',
                    help='Store a simple value')

args = parser.parse_args()

filein = args.file
fileout = args.output
mode = args.modevalue
countframes = args.countframes
positframes = args.positframes

####################
### OPENING FILE ###
####################

#open .avi file as binary
with open (filein, 'rb') as f: 
	## split the content at "idx1"
	a = f.read().split('idx1', 1)
	a1 = a[1]

	## get the length of the index and store it
	a1, idxl = a1[4:], a1[:4]

	## get the first iframe and store it
	n = 16
	iframe, a1 = a1[:n], a1[n:] 
	
	## put all frames in array
	b = [a1[i:i+n] for i in range(0, len(a1), n)] 
	
	## take out all of the sound frames cuz who gives a fuck
	sframeregex = re.compile(b'01wb\x10\x00\x00\x00.{8}')
	b = [x for x in b if not re.match(sframeregex,x)]

	## calculate number of frames
	c = len(b)

#########################
### OPERATIONS TO IDX ###
#########################

	### MODE - SHUFFLE 
	#####################

	if mode == "shuffle":
		idx = random.sample(b,c)

	### MODE - DELETE IFRAMES
	###########################

	if mode == "ikill":
		iframeregex = re.compile(b'00dc\x10\x00\x00\x00.{8}')
		idx = [x for x in b if not re.match(iframeregex,x)]

	### MODE - BLOOM
	##################

	if mode == "bloom":
		## bloom options
		repeat = int(countframes)	
		frame = int(positframes)
	
		## split list
		lista = b[:frame]
		listb = b[frame:]

		## rejoin list with bloom
		idx = lista + ([b[frame]]*repeat) + listb

	### MODE - P PULSE
	##################
	
	if mode == "pulse":
		pulselen = int(countframes)
		pulseryt = int(positframes)
	
		idx = [[x for j in range(pulselen)] if not i%pulseryt else x for i,x in enumerate(b)]
		idx = [item for sublist in idx for item in sublist]
		idx = ''.join(idx)
		idx = [idx[i:i+n] for i in range(0, len(idx), n)] 
	
	##just having fun by adding this at the end of the bloom
	#d = random.sample(d,c + repeat)

########################
### FIX INDEX LENGTH ###
######################## 

	print "old index size : " + str(c + 1) + " frames"
	hey = len(idx)*16
	print "new index size : " + str((hey/16) + 1) + " frames"

	## convert it to packed data
	idxl = struct.pack('<I',hey)

###################
### SAVING FILE ###
###################

	## rejoin the whole thing
	data = ''.join(a[0] + "idx1" + idxl + iframe + ''.join(idx)) 
	f = open(fileout, 'wb')
	f.write(data)
	f.close()
