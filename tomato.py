#!/bin/python3

import argparse
import re
import random
import struct

#################
### ARGUMENTS ###
#################

parser = argparse.ArgumentParser(description="whatever baby")
parser.add_argument("file", help="input file")
parser.add_argument("-o", "--output", help="output file")
args = parser.parse_args()

filein = args.file
fileout = args.output

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

	## calculate number of frames
	c = len(b)

#########################
### OPERATIONS TO IDX ###
#########################

	### MODE - SHUFFLE 
	#####################

	#d = random.sample(b,c)

	### MODE - DELETE IFRAMES
	###########################

	#iframeregex = re.compile(b'00dc\x10\x00\x00\x00.{8}')
	#d = [x for x in b if not re.match(iframeregex,x)]

	### MODE - BLOOM
	##################

	## bloom options	
	frame = 55
	repeat = 500

	## split list
	lista = b[:frame]
	listb = b[frame:]

	## rejoin list with bloom
	d = lista + ([b[frame]]*repeat) + listb

	##just having fun by adding this at the end of the bloom
	d = random.sample(d,c + repeat)

########################
### FIX INDEX LENGTH ###
######################## 

	print "old index size : " + str(c + 1) + " frames"
	hey = len(d)*16
	print "new index size : " + str((hey/16) + 1) + " frames"

	## convert it to packed data
	idxl = struct.pack('<I',hey)

###################
### SAVING FILE ###
###################

	## rejoin the whole thing
	data = ''.join(a[0] + "idx1" + idxl + iframe + ''.join(d)) 
	f = open(fileout, 'wb')
	f.write(data)
	f.close()

