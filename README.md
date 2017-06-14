# tomato

**tomato** is a python script and datamoshing kit for AVI files 
- utilities inspired by [Way Spurr-Chen](https://github.com/wayspurrchen)'s [moshy](https://github.com/wayspurrchen/moshy). 
- functionality based off of [Tomasz Sulej](https://github.com/tsulej)'s research on AVI file structure.

It was designed to operate video frame ordering, substraction and duplication.

- `ikill` - destroys all of the i-frames
- `iswap` - retreats all of the i-frames one sequence earlier [under construction: whole mode not programmed]
- `bloom` - duplicates `c` times p-frame number `n`
- `pulse` - duplicates groups of `c` p-frames every `n` frames
- `shuffle` - every p-frame gets a `p` % chance to be shuffled [under construction: -p not available]

>regardless of the option used the 1st iframe of the video will remain unaffected

## Examples of usage

>python tomato.py -i input.avi -m ikill output.avi

>python tomato.py -i input.avi -m bloom -c 50 -n 100 output.avi 

Takes the 100th video frame and duplicate 50 times

>python tomato.py -i input.avi -m pulse -c 5 -n 10 output.avi 

Duplicates every 10th frame 5 times

>python tomato.py -i input.avi -m shuffle output.avi

Shuffles all of the frames in the video

## Why did I develop tomato ?

Most datamoshing utilities out there are pretty cool but restrain you into using specific codecs or just can't handle big files and/or large resolutions.

tomato is different in the sense that

+ it can be used with any AVI file regardless of the codec/resolution
+ it doesn't corrupt the video content, just the stream
+ it's **a lot** faster than anything else

However there is still room for improvement

- it can't act on AVI files that do not have an index
(which means I should add options to force an index creation, or divide a video if it is over >4GB) 

## So how does it work ?

Basically when you input an AVI file, it ignores the content and skips to the frame index to operate on it.
Video players reading the resulting file through the index will interpret and glitch the video on the fly.

For practicles purposes sounds frames are all deleted

## How should you use it

No dependencies are needed to run tomato but I recommend preparing your AVI files with ffmpeg and the codec library of your choice.
To read your glitched files I recommend VLC or Xine if you're under Linux. Both are great for visualazing content (especially xine for the shuffle mode) but keep in mind you should always be experimenting and using different visualizers or tools to bake your files.
If you have any questions or ideas feel free to send me an email at kaspar.ravel@gmail.com
