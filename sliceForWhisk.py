'''
# methods clock first file
clock second file substract pole in (being trigger of the pole then light on light off after 5 seconds then pole takes roughly 5 seconds ) for pole in 

pole out the sequence is ligth on (5 seconds) then light off and pole start to come out when light off
'''

# this can be useful to 
'''import pims
file = r"Y:\Sheldon\Highspeed\not_analyzed\WDIL009\close_position\26_d.seq"
v = pims.Video(file, as_raw=True)
'''

import pandas as pd
import glob
import os
import subprocess
import concurrent.futures
import time

def convert(secondsInput): 
    seconds = secondsInput % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%02d:%02d:%02d" % (hour, minutes, seconds), (hour*3600+minutes*60+int('%02d'% seconds))*500 
    # the milliseconds formating below does not provide exact slicing of the video 
    #"%02d:%02d:%#06.3f" % (hour, minutes, seconds) 

class mp4ToSlice:
    '''
    work on class of object to be able to extract all the information from the video to be able to be sliced
    '''
    def __init__(self, file):
        '''initial method that takes the file of  interest to be able to be recovered '''
        self.file = file # name of the file
        self.aid = file.split(os.sep)[-1].split('_')[0]

        pathFolder = file.split(os.sep)
        self.folder = os.sep.join(pathFolder[:-1])

    def getTimeFiles(self):
        if 'd' in self.file.split(os.sep)[-1]:
            pathTotime = glob.glob(self.folder+os.sep+'*dark*')[0]
        elif 'l' in self.file.split(os.sep)[-1]:
            pathTotime = glob.glob(self.folder+os.sep+'*light*')[0]

        # get the files 
        timeFilesa = glob.glob(pathTotime+os.sep+self.aid+os.sep+'*pole*.csv')
        if timeFilesa == []:
            a = pd.DataFrame({'normFrameCorrectedFFMPEG':[57000.0, 119500.0, 177000.0, 239500.0, 297000.0, 359500.0]})
            a['ephochPole'] = [1,1,2,2,3,3]
            a['timeSlice'] = ['00:01:54', '00:03:59', '00:05:54', '00:07:59', '00:09:54', '00:11:59']
        
        else:
            a = pd.read_csv(timeFilesa[0])
            
            if a.shape != (1, 12):
            # this is to correct for the file type that is present some have are 1x12 others are 3x4
                 a = pd.DataFrame({'dat':a.iloc[:,[1,3]].values.flatten()})

            a = a.iloc[0]
            a = pd.DataFrame({'dat':a.reset_index(drop=True)})
            a = a[a['dat'] != True]

            b = pd.read_csv(glob.glob(pathTotime+os.sep+self.aid+os.sep+'*eye_cam*.csv')[0])
            zeroDat = b.iloc[0,1]
            a['normTime_sec'] = a['dat']-zeroDat
            a['normFrame'] = (a['normTime_sec']*500).astype(int)
            a['poleStatus'] = poleStatus = ['in', 'out']*3

            # this is to accomodate a 3 seconds jitter around the point of interest
            # that can be necessary due to the 
            a.loc[a['poleStatus']=='in','normFrameCorrected'] = a.loc[a['poleStatus']=='in','normFrame']-5*500
            a.loc[a['poleStatus']=='out','normFrameCorrected'] = a.loc[a['poleStatus']=='out','normFrame']+5*500

            # convert the data frame to be able to extract the time for which the video should be chuncked
            a = pd.merge(a, (a['normFrameCorrected']/500).apply(lambda x: pd.Series(convert(x), index =['timeSlice', 'normFrameCorrectedFFMPEG'])), how='inner', left_index=True, right_index=True)
            a['ephochPole'] = [1,1,2,2,3,3]

        return a

# get the series of time 
def conversionSlice(fileName):

    t = mp4ToSlice(fileName)
    timePoleEpoch = t.getTimeFiles()

    for i in range(1,4):
        print(i)
        tmp = timePoleEpoch.loc[timePoleEpoch['ephochPole'] == i, 'timeSlice'].values
        tmpRef = timePoleEpoch.loc[timePoleEpoch['ephochPole'] == i, 'normFrameCorrectedFFMPEG'].values.astype(int)
        testFile = t.file
        newName = os.sep.join(testFile.split(os.sep)[:-1])+os.sep+testFile.split(os.sep)[-1].split('.')[0]+'_p'+str(i)+'_'+str(tmpRef[0])+'-'+str(tmpRef[1])+'.mp4'
        print(newName)
        subprocess.call('ffmpeg -i ' + testFile + ' -codec:v mpeg4 -r 500 -qscale:v 4 -codec:a copy -video_track_timescale 500 -ss '+ tmp[0]+ ' -to '  +tmp[1] +' '+ newName , shell=True)

##################333 USER INPUT ###########################
# mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
# files = glob.glob(mainPath+'/**/*.mp4')

mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009\middle_position'
files = glob.glob(mainPath+os.sep+'25_d.avi')
print(files)
##################333 USER INPUT ###########################

with concurrent.futures.ProcessPoolExecutor() as executor:
    if __name__ == '__main__':
        executor.map(conversionSlice, files)
