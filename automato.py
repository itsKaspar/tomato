import argparse, os, re, random, struct, time
from moviepy.editor import VideoFileClip

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-i", "--input", help="input file")
parser.add_argument('-m', "--mode", action='store', dest='modevalue',help='choose mode, one of:\nshuffle irep ikill bloom pulse reverse invert')
parser.add_argument('-c', action='store', dest='countframes',help='var1', default=1)
parser.add_argument('-n', action='store', dest='positframes',help='var2', default=1)
parser.add_argument('-l','--lim', help='fraction of file to search before giving up, default: 4', default=4)
parser.add_argument("-c:v", "--vcodec", action='store', dest='vidcodec', help="codec and settings")
parser.add_argument("file", help="input file")

args = parser.parse_args()

filein = args.input
filename = filein.rsplit( ".", 1 )[ 0 ] #strip extension
clip = VideoFileClip(filein)
mode = args.modevalue
countframes = args.countframes
positframes = args.positframes
vidcodec = args.vidcodec

if vidcodec == "libxvid":
	vidcodec = "libxvid -qscale:v 1"

########################################
##### CREATE ALL DIRS FOR PROJECT ######
########################################

if not os.path.exists("automato-" + filename): 
	os.makedirs("automato-" + filename)

if not os.path.exists("automato-" + filename + "/enc"): 
	os.makedirs("automato-" + filename + "/enc")	
	
if not os.path.exists("automato-" + filename + "/glitched"): 
	os.makedirs("automato-" + filename + "/glitched")
	
if not os.path.exists("automato-" + filename + "/baked1"): 
	os.makedirs("automato-" + filename + "/baked1")
	
if not os.path.exists("automato-" + filename + "/baked2"): 
	os.makedirs("automato-" + filename + "/baked2")

########################################
##### CUT + ENCODE VIDEO INTO SMALL PARTS #######
########################################	

i = 0
tracker = 0 #current seconds in the movie file
out_dir = "automato-" + filename  + "/enc"
filez = 0

cliplength = int(clip.duration)

while(tracker < cliplength - 1):
	os.system("ffmpeg -ss " + str(tracker) +  " -i " + filein + " -fs 500000000 -c:v " + vidcodec + " -an -bf 0 -g 99999 " + out_dir + "/enc_" + filename + "_" + str(i) + ".avi")
	
	lastcut = VideoFileClip(out_dir + "/enc_" + filename + "_" + str(i) + ".avi")
	tracker = tracker + lastcut.duration
	i += 1
	filez += 1
		
########################################
##### TOMATO ALL VIDEOS ################
########################################

i = 0
in_dir = "automato-" + filename + "/enc"
out_dir = "automato-" + filename  + "/glitched"

while i < filez :
	os.system("python tomato.py -i " + in_dir + "/enc_" + filename + "_" + str(i) + ".avi -m " + mode + " -c " + countframes + " -n " + positframes + " " + out_dir + "/glitched_" + filename + "_" + str(i) + ".avi")
	i += 1


########################################
##### BAKE ALL VIDEOS ##################
########################################

i = 0
in_dir = "automato-" + filename + "/glitched"
out_dir = "automato-" + filename  + "/baked1"
while i < filez :
	os.system("mencoder " + in_dir + "/glitched_" + filename + "_" + str(i) + ".avi -o " + out_dir + "/baked1_" + filename + "_" + str(i) + ".mov -ovc x264")
	i += 1
	time.sleep(5)
	
i = 0
in_dir = "automato-" + filename + "/baked1"
out_dir = "automato-" + filename + "/baked2"
while i < filez :
	os.system("ffmpeg -i " + in_dir + "/baked1_" + filename + "_" + str(i) + ".mov -c:v libx264 " + out_dir + "/baked2_" + filename + "_" + str(i) + ".mov")
	i += 1

########################################
##### JOIN ALL VIDEOS ##################
########################################

in_dir = "automato-" + filename + "/baked2"

concatfile = open("automato-" + filename + "/concat_" + filename + ".txt", "w")
concatfile.close()
i = 0

while i < filez :
	concatfile = open("automato-" + filename + "/concat_" + filename + ".txt", "a")
	concatfile.write("file baked2/baked2_" + filename + "_" + str(i) + ".mov'")
	concatfile.write("\n")
	concatfile.close()
	i += 1

if filez > 1:
	os.system("ffmpeg -f concat -safe 0 -i automato-" + filename + "/concat_" + filename + ".txt -c copy automato-" + filename + "/FINAL_" + filename + ".mp4")
else:
	os.system("ffmpeg -i " + in_dir + "/baked2_" + filename + "_" + str(i) + ".mov -c copy automato-" + filename + "/FINAL_" + filename + ".mp4")
	
	
	
