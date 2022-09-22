import pandas as pd
import glob
import os
import subprocess
import concurrent.futures
import time

# could be worht a read for future improvements
# https://towardsdatascience.com/faster-video-processing-in-python-using-parallel-computing-25da1ad4a01



##################### USER INPUT #########################################
## to convert all the avi 

print('')
print('If the directories have spaces in the name that will create a problem')
print('videos with spaces will be renamed to underscore')

print('-------------------------------------------')
print('Select the main folders where the videos are located')
mainPath = input("Drag the FOLDER and press Enter:")
mainPath = mainPath.replace('\\','/')
mainPath = mainPath.replace('"','')

print('')
print('-------------------------------------------')
fileFormat = input("Type of video files (eg: avi, mp4):")


print('Select folder location')
mainOut = input("The letter of the drive where videos should be saved. Note that the tree structure would be replacted (eg: Y)")
mainOut = [mainOut+':']### need to change the main output drive
files = glob.glob(mainPath+'/**/*.'+fileFormat, recursive=True)



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

def nameNew(fileName, mainOut):
    tmpStruc = fileName.split(os.sep)
    tmptest = mainOut
    for i in tmpStruc[1:-1]:
        tmptest.append(i)
        newdir = os.sep.join(tmptest)
        # print(newdir)
        os.makedirs(newdir, exist_ok = True)
        # print(newdir)

    ## convert all the files with spaces to files with underscore to 
    ## enable proper function of ffmpeg if not then this would lead to an error
    fileOri = fileName
    fileNameDir = os.path.dirname(fileName)
    fileName = fileName.split(os.sep)[-1].replace(" ", '_')
    os.rename(fileOri, fileNameDir+os.sep+fileName)
    nfileNameOri = fileNameDir+os.sep+fileName
    nfileName = fileName.split(os.sep)[-1].split('.')[0]+'.mp4'
    nfileName = newdir+os.sep+nfileName
    # folderNameSplit = fileName.split(os.sep)
    # folderNameSplit = os.sep.join(folderNameSplit[1:-1])
    # fileName = fileName.split(os.sep)[-1].split('.')[0]+'.mp4'
    # folderName = r'C:\Users\Windows\Desktop\SpeedUPVID'+os.sep+folderNameSplit
    # fileName = folderName+os.sep+fileName
    # os.makedirs(folderName, exist_ok=True)
    return nfileNameOri, nfileName

def tmpFct(file):
    file, newi = nameNew(file, mainOut)

    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    ''' Conversion note 
    -codec:v : mpeg4 necessary to be able to have good fps tbn tbr matching
    -r: enables to have the frame rate of intres
    -qscale:v: this is the quality of the video
    -codec:a: needed to have audio codec
    -video_track_timescale: force the tbn value
    '''
    ## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # os.chdir(os.path.dirname(file))
    # fileBN = file.split(os.sep)[-1]
    subprocess.call('ffmpeg -i ' + file + ' -codec:v mpeg4 -r 475 -qscale:v 4 -codec:a copy -video_track_timescale 475 '+ newi , shell=True)
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
    subprocess.call('ffmpeg -i ' + file + ' -codec:v mpeg4 -r 475 -qscale:v 4 -codec:a copy -video_track_timescale 475 '+ newi , shell=True)
    print(file, newi)

## to redo the files
#mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009\close_position'
#files = glob.glob(r"Y:\Sheldon\Highspeed\not_analyzed\WDIL009\Archive\close_position\25_d.avi")
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