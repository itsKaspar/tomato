# tomato

**tomato** is a python script to glitch AVI files 
- utilities inspired by [Way Spurr-Chen](https://github.com/wayspurrchen)'s [moshy](https://github.com/wayspurrchen/moshy). 
- functionality based off of [Tomasz Sulej](https://github.com/tsulej)'s research on AVI file structure.

It was designed to operate video frame ordering, substraction and duplication.

Modes called through -mode [mode]

- `void` - does nothing
- `random` - randomizes frame order
- `reverse` - reverse frame order
- `invert` - switches each consecutive frame witch each other
- `bloom` - duplicates `c` times p-frame number `n`
- `pulse` - duplicates groups of `c` p-frames every `n` frames
- `overlap` - copy group of `c` frames taken from every `n`th position
- `jiggle` - take frame from around current position. `n` parameter is spread size [broken]

Other parameters :

- `-c and -n` - reserved for the modes
- `-ff [0 or 1]` - ignore first frame (default 1)
- `-a [0 or 1]` - activate audio (default 0)
- `-k [0 to 1]` - kill frames with too much data (default 0.7)

## Examples of usage

Takes out iframes:
>python tomato.py -i input.avi

Duplicate 50 times the 100th frame:
>python tomato.py -i input.avi -m bloom -c 50 -n 100 

Duplicates 5 times a frame every 10 frame:
>python tomato.py -i input.avi -m pulse -c 5 -n 10

Shuffles all of the frames in the video:
>python tomato.py -i input.avi -m random

Copy 4 frames taken starting from every 2nd frame. [1 2 3 4 3 4 5 6 5 6 7 8 7 8...]:
>python tomato.py -i input.avi -m overlap -c 4 -n 2


## Why tomato ?

I made tomato because I wanted to be able to glitch avi files regardless of the contained codec, the resolution and the file size while still being super duper fast and not needing to encode anything.

## How does it work ?

It reorders the frames inside the movi tag of your AVI file.

## How should you use it

Libraries used : numpy, argparse, os, re, random, struct, itertools

I recommend preparing your AVI files with ffmpeg and the codec library of your choice. To read your glitched files I recommend VLC or Xine if you're under Linux. Both are great for visualizing content (especially xine for the random mode) but keep in mind you should always be experimenting and using different visualizers or tools to bake your files.

If you have any questions or ideas feel free to send me an email at kaspar.ravel@gmail.com

For more info on development : https://www.kaspar.wtf/blog/tomato-v2-0-avi-breaker
