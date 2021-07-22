# Highspeed video compression

## Introduction

This is a set of scripts to facilitate the management of acquisition video and ensuring there proper encoding with software like [whisk](https://github.com/nclack/whisk)

The main objective is to obtain readable video that can be compressed while retaining software compatibility. As some of the highspeed video aquired are 

## Process 
1. Acquire highspeed video with StreamPix (Norpix software) as `*.seq` file
2. Use batch conversion utilities from StreamPix (Norpix software) to convert `*.seq` to `*.avi`
3. Convert/encode the `*.avi` to `*.mp4` using [ffmpeg](https://ffmpeg.org/)
	- windows open `cmd`
	- go to the folder (with `cd`) where the script `avi2mp4.py` is located
	- run the script `python avi2mp4.py`
	- for `-qscale:v 10` this enables the conversion of 14Tb --> 0.04Tb (44Gb) overnight CPU based with IntelCore i9-9820X CPU @ 3.30GHz 10 cores. The `mpeg4` encoding is not suported with GPU encoding.
	- for `-qscale:v 4` this enables the conversion of 14Tb --> 0.19Tb (190Gb) overnight CPU based with IntelCore i9-9820X CPU @ 3.30GHz 10 cores. The `mpeg4` encoding is not suported with GPU encoding.

## Downstream analysis

### Analysis with whisk
**important consideration:**
	- we encountered memory issues when running long highspeed video with whisk thus the video can be sliced 
	- encoding is critical to have tbc, tbn and tbr consistent (see whisk issues [here](https://github.com/nclack/whisk/issues/35))  

**key points for ffmpeg usage:**
	`-codec:v`: mpeg4 necessary to be able to have good fps tbn tbr matching  
	`-r`: enables to have the frame rate of intres  
	`-qscale:v`: this is the quality of the video (from 1 highest quality/larger file to 31 smallest quality/smaller file)  
	`-codec:a`: needed to have audio codec  
	`-video_track_timescale`: force the tbn value  

1. slice the video with `sliceForWhisk.py`
2. use [git Bash](https://gitforwindows.org/)
3. setup GNU parallel for Windows [see](https://www.gnu.org/software/parallel/)
	- for install see []
	- [tutorial](https://www.gnu.org/software/parallel/parallel_tutorial.html)
4. run bash script for parallel analysis of the task
	- see [`bashForWhisk.sh` ](https://github.com/wAOndering/HSvideoManagement/blob/main/bashForWhisk.sh)
	- *TODO: complete and improve the script*
	- *TODO: better naming convention*
	- *TODO: run script one after the other*



