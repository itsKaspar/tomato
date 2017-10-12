#!/usr/bin/python2.7

import argparse, os, re, random, struct
from itertools import chain

print " _                        _        "
print "| |                      | |       "
print "| |_ ___  _ __ ___   __ _| |_ ___  "
print "| __/ _ \| '_ ` _ \ / _` | __/ _ \ "
print "| || (_) | | | | | | (_| | || (_) |"
print " \__\___/|_| |_| |_|\__,_|\__\___/ "
print "tomato.py v1.3 last update 12.10.2017"
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
parser.add_argument('-m', "--mode", action='store', dest='modevalue',help='choose mode, one of:\nshuffle irep ikill bloom pulse reverse invert')
parser.add_argument('-c', action='store', dest='countframes',help='var1', default=1)
parser.add_argument('-n', action='store', dest='positframes',help='var2', default=1)
parser.add_argument('-l','--lim', help='fraction of file to search before giving up, default: 4', default=4)
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
	filesize = os.path.getsize(filein)
	chunk = 1024
	lim = args.lim
	idx = ''
	with open(fileout,'wb') as wr:
		print "Streaming File\n"
		for pos in xrange(filesize-chunk, filesize-filesize/lim, -chunk): # move backwards through data
			rd.seek(pos)
			buffer = rd.read(chunk)

			if buffer.find(b'idx1') >= 0:
				split = buffer.split(b'idx1', 1)
				rd.seek(0)
				wr.write(rd.read(pos)) # start the read at the beginning again,
				wr.write(split[0])  # spit out data up to this point plus the stuff before idx
                                rd.seek(len(split[0])+4,1)
				idx = rd.read()
				break

		if len(idx) == 0:
			print('Could not locate index!\n')
			raise SystemExit # quit


	print "Getting list of Tomatoes\n"
	## get the length of the index and store it
	idx, index_length = idx[4:], idx[:4]

	## get the first iframe and store it
	n = 16
	first_frame, idx = idx[:n], idx[n:]
	check = bytearray()
 	check.extend(first_frame)
	#print([i for i in check])
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

		nidx = []
		last = None
		regex = re.compile(b'.*dc\x10.*')
		for x in idx:
			if not last: last = x
			if not re.match(regex,x):
				nidx.append(x)
				last = x
			else:
				nidx.append(last)
		idx = nidx

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
	print "new index size : " + str((index_length/16)) + " frames\n"

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

	print "Your file has been saved <3\n"
	print "Prefer VLC to view your unstable video file"
	print "But don't forget to bake it ! :)"

#############
### DEBUG ###
#############

## creates a seperate file with the index

#	f3 = open('index.avi', 'wb')
#	f3.write(''.join(idx))
