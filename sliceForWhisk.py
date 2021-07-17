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

def convert(secondsInput): 
    seconds = secondsInput % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%02d:%02d:%02d" % (hour, minutes, seconds), (hour*3600+minutes*60+int('%02d'% seconds))*500 
    # the milliseconds formating below does not provide exact slicing of the video 
    #"%02d:%02d:%#06.3f" % (hour, minutes, seconds) 


mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009\close_position\close_bonsai_dark'
# mainPath = '/run/user/1000/gvfs/smb-share:server=ishtar,share=millerrumbaughlab/Sheldon/Highspeed/not_analyzed/WDIL009/close_position/close_bonsai_dark' 


files = glob.glob(mainPath+os.sep+'**/*.csv', recursive=True)

files = [x for x in files if os.sep+'34'+os.sep in x]




poleStatus = ['in', 'out']*3

# def reformatPoleTime(pdDF):

a = pd.read_csv(files[0])
a = a.iloc[0]
a = pd.DataFrame({'dat':a.reset_index(drop=True)})
a = a[a['dat'] != True]


b = pd.read_csv(files[1])
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




# get the series of time 
for i in range(1,4):
    print(i)
    tmp = a.loc[a['ephochPole'] == i, 'timeSlice'].values
    tmpRef = a.loc[a['ephochPole'] == i, 'normFrameCorrectedFFMPEG'].values.astype(int)
    testFile = r'C:\Users\Windows\Desktop\cutTestFUll\34_d.mp4'
    newName = os.sep.join(testFile.split(os.sep)[:-1])+os.sep+testFile.split(os.sep)[-1].split('.')[0]+'_p'+str(i)+'_'+str(tmpRef[0])+'-'+str(tmpRef[1])+'.mp4'
    print(newName)


    subprocess.call('ffmpeg -i ' + testFile + ' -codec:v mpeg4 -r 500 -qscale:v 10 -codec:a copy -ss '+ tmp[0]+ ' -to '  +tmp[1] +' '+ newName , shell=True)









# subprocess.call('ffmpeg -i '+tmp+' -ss 01:08:10 -to 01:23:00 cut_'+tmp, shell=True)

# testFile = r'C:\Users\Windows\Desktop\cutTestFUll\34_d.mp4'
# newName = os.sep.join(testFile.split(os.sep)[:-1])+os.sep+testFile.split(os.sep)[-1].split('.')[0]+'_p'+str(i)+'_'+str(tmpRef[0])+'-'+str(tmpRef[1])+'.mp4'

# testFile = r'C:\Users\Windows\Desktop\cutTestFUll\34_d.mp4'
# newName = testFile.split(os.sep)[0]+testFile.split(os.sep)[-1]
