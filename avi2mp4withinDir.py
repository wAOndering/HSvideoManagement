
import pandas as pd
import glob
import os
import subprocess
import concurrent.futures
import time


mainPath = r'Y:\Jessie\e3 - Data Analysis\e3 Data\allVideos\avi_Process'
os.chdir(mainPath)
files = glob.glob('*.avi')


def nameNew(fileName):
    fileName = fileName.split('.')[0]+'.mp4'
    # folderNameSplit = fileName.split(os.sep)
    # folderNameSplit = os.sep.join(folderNameSplit[1:-1])
    # fileName = fileName.split(os.sep)[-1].split('.')[0]+'.mp4'
    # folderName = r'C:\Users\Windows\Desktop\SpeedUPVID'+os.sep+folderNameSplit
    # fileName = folderName+os.sep+fileName
    # os.makedirs(folderName, exist_ok=True)
    return fileName

def tmpFct(file):
    newi = nameNew(file)

    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ''' Conversion note 
    -codec:v : mpeg4 necessary to be able to have good fps tbn tbr matching
    -r: enables to have the frame rate of intres
    -qscale:v: this is the quality of the video
    -codec:a: needed to have audio codec
    -video_track_timescale: force the tbn value
    '''
    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # subprocess.call('ffmpeg -i ' + file + ' -codec:v mpeg4 -r 500 -qscale:v 4 -codec:a copy -video_track_timescale 500 '+ newi , shell=True)
    subprocess.call('ffmpeg -i ' + file + ' -vcodec libx264 -crf 20 '+ newi , shell=True)
    print(file, newi)


with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        executor.map(tmpFct, files)

finish = time.perf_counter()
print("Finished in time : ", finish)