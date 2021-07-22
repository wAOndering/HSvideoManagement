import pandas as pd
import glob
import os
import subprocess
import concurrent.futures
import time

# could be worht a read for future improvements
# https://towardsdatascience.com/faster-video-processing-in-python-using-parallel-computing-25da1ad4a01

def checkFileSize(listoffiles):
    sizeAll = []
    for i in listoffiles:
        size = os.path.getsize(i)
        sizeAll.append(size)
    sizeAll = sum(sizeAll)*10**-9 # get the sum of all the files 
    # useful for file size
    # https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    # print ('{:,.0f}'.format(os.path.getsize(sizeAll)/float(1<<30))+" GB")
    print('file size is ', sizeAll, 'GB')
    return sizeAll

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
    subprocess.call('ffmpeg -i ' + file + ' -codec:v mpeg4 -r 500 -qscale:v 4 -codec:a copy -video_track_timescale 500 '+ newi , shell=True)
    print(file, newi)

def filestoReDo(filesList, lowlim = 100*10**6):
    sizeAll = []
    for i in filesList:
        size = os.path.getsize(i)
        dat = pd.DataFrame({'fileName': [i], 'size': [size]})
        # print(dat)
        sizeAll.append(dat)

    sizeAll = pd.concat(sizeAll)
    deletelist = list(sizeAll.loc[sizeAll['size'] <= lowlim, 'fileName'])

    redolist= []
    for i in deletelist:
        tmp = i.split('.')[0]+'.avi'
        os.remove(i)
        redolist.append(tmp)


    return redolist, deletelist


    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ''' Conversion note 
    -codec:v : mpeg4 necessary to be able to have good fps tbn tbr matching
    -r: enables to have the frame rate of intres
    -qscale:v: this is the quality of the video
    -codec:a: needed to have audio codec
    -video_track_timescale: force the tbn value
    '''
    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subprocess.call('ffmpeg -i ' + file + ' -codec:v mpeg4 -r 500 -qscale:v 4 -codec:a copy -video_track_timescale 500 '+ newi , shell=True)
    print(file, newi)


##################### USER INPUT #########################################
## to convert all the avi 
# mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\HS010_Rum2'
files = glob.glob(mainPath+'/**/*.avi')

## to redo the files
# mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009\close_position'
# files = glob.glob(mainPath+'/28_d*.avi')
# print(files)
# files, deletelist = filestoReDo(files)


## to redo the files
# files = ['Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\35_l.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\36_d.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\36_l.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\37_d.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\37_l.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\38_d.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\38_l.avi',
#  'Y:\\Sheldon\\Highspeed\\not_analyzed\\WDIL009\\close_position\\39_d.avi']
##################### USER INPUT #########################################

with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        executor.map(tmpFct, files)

finish = time.perf_counter()
print("Finished in time : ", finish)