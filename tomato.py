#!/bin/python2.7

import argparse
import re
import random
import struct
from itertools import chain

print " _                        _        "
print "| |                      | |       "
print "| |_ ___  _ __ ___   __ _| |_ ___  "
print "| __/ _ \| '_ ` _ \ / _` | __/ _ \ "
print "| || (_) | | | | | | (_| | || (_) |"
print " \__\___/|_| |_| |_|\__,_|\__\___/ "
print "tomato.py v1.1 last update 19.07.2017"
print "\\\\ Audio Video Interleave index breaker"
print " "
print "\"je demande a ce qu'on tienne pour un cretin"
print "celui qui se refuserait encore, par exemple,"
print "a voir un cheval galoper sur une tomate.\""
print " - Andre Breton"
print " "
print "___________________________________"
print " "

#################
### ARGUMENTS ###
#################

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-i", "--input", help="input file")
parser.add_argument('-m', "--mode", action='store', dest='modevalue',help='choose mode')
parser.add_argument('-c', action='store', dest='countframes',help='var1', default=1)
parser.add_argument('-n', action='store', dest='positframes',help='var2', default=1)
parser.add_argument("file", help="input file")

args = parser.parse_args()

fileout = args.file
filein = args.input
mode = args.modevalue
countframes = args.countframes
positframes = args.positframes

####################
### OPENING FILE ###
####################

with open(filein,'rb') as rd:
	print "Opening File\n"
	with open(fileout,'wb') as wr:
		print "Streaming File\n"
		while True:
			buffer = rd.read(1024)
			if buffer: 
				if buffer.find(b'idx1') == -1 : 
					for byte in buffer :
						wr.write(byte)
				else:
					splitidx = buffer.split(b'idx1', 1)
					wr.write(splitidx[0])
					idx = splitidx[1] + rd.read()
					break
			else:
				print('file has no index')
				break
	wr.close()

	print "Getting list of Tomatoes\n"
	## get the length of the index and store it
	idx, index_length = idx[4:], idx[:4]

	## get the first iframe and store it
	n = 16
	first_frame, idx = idx[:n], idx[n:]
	check = bytearray()
	check.extend(first_frame)
	print([i for i in check])
	## put all frames in array ignoring sound frames
	regex = re.compile(b'.*wb.*')
	idx = [idx[i:i+n] for i in range(0, len(idx), n) if not re.match(regex,idx[i:i+n])] 	

	## calculate number of frames
	number_of_frames = len(idx)

	print "Ready for the serious shitz\n"
	
#########################
### OPERATIONS TO IDX ###
#########################

	if mode == "void":
		print "### MODE - VOID"
		print "##################\n"
		
		print "not doing shit"
		
	if mode == "shuffle":
		print "### MODE - RANDOM"
		print "##################\n"
		idx = random.sample(idx,number_of_frames)

	if mode == "ikill":
		print "### MODE - IKILL"
		print "##################\n"
		regex = re.compile(b'.*dc\x10.*')
		idx = [x for x in idx if not re.match(regex,x)]

	if mode == "irep":
		print "### MODE - IREP"
		print "##################\n"
		
		idx = []
		last = None
		regex = re.compile(b'.*dc\x10.*')
		for x in idx:
			if not last: last = x
			if not re.match(regex,x):
				idx.append(x)
				last = x		
			else:
				idx.append(last)

	if mode == "bloom":
		print "### MODE - BLOOM"
		print "##################\n"
		## bloom options
		repeat = int(countframes)	
		frame = int(positframes)
	
		## split list
		lista = idx[:frame]
		listb = idx[frame:]

		## rejoin list with bloom
		idx = lista + ([idx[frame]]*repeat) + listb
	
	if mode == "pulse":
		print "### MODE - PULSE"
		print "##################\n"
		
		pulselen = int(countframes)
		pulseryt = int(positframes)
	
		idx = [[x for j in range(pulselen)] if not i%pulseryt else x for i,x in enumerate(idx)]
		idx = [item for sublist in idx for item in sublist]
		idx = ''.join(idx)
		idx = [idx[i:i+n] for i in range(0, len(idx), n)] 
	
	if mode == "reverse":	
		print "### MODE - REVERSE"
		print "##################\n"
		
		idx = idx[::-1]
	
	if mode == "invert":	
		print "### MODE - INVERT"
		print "##################\n"
		
		idx = sum(zip(idx[1::2], idx[::2]), ())

########################
### FIX INDEX LENGTH ###
######################## 

	print "old index size : " + str(number_of_frames + 1) + " frames"
	index_length = len(idx)*16 + 16
	print "new index size : " + str((index_length/16) + 1) + " frames\n"

	## convert it to packed data
	index_length = struct.pack('<I',index_length)

###################
### SAVING FILE ###
###################

	print "Saving new file\n"
	## rejoin the whole thing
	data = b''.join(b'idx1' + index_length + first_frame + b''.join(idx)) 
	wr = open(fileout, 'ab')
	wr.write(data)
	wr.close()
	
	print "Your file has been saved <3 remember to bake it !\n"

#############
### DEBUG ###
#############

## creates a seperate file with the index
	
#	f3 = open('index.avi', 'wb')
#	f3.write(''.join(idx))
