import glob
import os
import pandas as pd
import numpy as np


def commonElement(list1, list2, option='dext'):
	'''
	function to identify common element in the list
	option: 'dext' enables to look at the basefilename without the extension useful to check if the files
	were in deed compressed
	'''
	if len(list1)<len(list2):
		tmp = list1
		list1 = list2
		list2 = list1
	
	list1Name = os.path.dirname(list1[0]) 
	list2Name = os.path.dirname(list2[0])
	
	if option == 'dext':
		# modification takes care of multi period in the path 
		list1 = [('.').join(x.split(os.sep)[-1].split('.')[:-1]) for x in list1]
		list2 = [('.').join(x.split(os.sep)[-1].split('.')[:-1]) for x in list2]
		# list1 = [x.split(os.sep)[-1].split('.')[0] for x in list1]
		# list2 = [x.split(os.sep)[-1].split('.')[0] for x in list2]

	commonElem = [x for x in list1 if x in list2]

	print('There are', len(commonElem), 'out of', max(len(list1), len(list2)), 'files which are common')
	print('For', list1Name, ':')
	print(len(commonElem), 'out of', len(list1), 'files which are common')
	print('For', list2Name, ':')
	print(len(commonElem), 'out of', len(list2), 'files which are common')

	notcommonElem = [x for x in list2 if x not in list1]
	# alternatively could use np.setdiff1d(list1, list2)
	print('None common elements present in', list2Name, ' : ')
	print(notcommonElem)


	## toDel = [os.remove(''.join([list2Name,os.sep,x,'.avi'])) for x in commonElem]


	# return notcommonElem




def getSize(filesList):
	sizeAll = []
	for i in filesList:
	    size = os.path.getsize(i)
	    dat = pd.DataFrame({'fileName': [i], 'size': [size]})
	    # print(dat)
	    sizeAll.append(dat)

	sizeAll = pd.concat(sizeAll)
	sumAll = sizeAll['size'].sum()*10**-12
	print('The total file size is : ', sumAll, ' TB')

	return sizeAll	

def archiveDatFct(file):
	'''
	this function is to split a path into its useful components
	''' 
	customName = 'Archive'
	fileSplit = file.split(os.sep)
	os.makedirs(os.sep.join(fileSplit[:-2])+os.sep+customName+os.sep+fileSplit[-2], exist_ok=True)
	archName = os.sep.join(fileSplit[:-2])+os.sep+customName+os.sep+os.sep.join(fileSplit[-2:])
	
	os.rename(file, archName)





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

redolist, deletelist = filestoReDo(files)

def checkFileConversionAviMp4(mainPath, position):
	## check for the first conversion form avi to mp4
    avifiles = glob.glob(mainPath+'/'+position+'/*.avi')
    aviId = np.unique([x.split(os.sep)[-1].split('.')[0] for x in avifiles])
    
    mp4filesUnsliced = glob.glob(mainPath+'/'+position+'/*[l,d].mp4')
    mp4filesUnslicedId = np.unique([x.split(os.sep)[-1].split('.')[0] for x in mp4filesUnsliced])

    print('avi to mp4 step for : ', position)
    commonElement(aviId, mp4filesUnslicedId, 'no')
    print('')

	# list(mp4filesUnslicedId)*3

	## check for the first conversion form avi to mp4
    mp4filesSliced = glob.glob(mainPath+'/'+position+'/*_p[1-3]*.mp4')
    mp4filesSlicedId = np.unique([x.split(os.sep)[-1].split('.')[0].split('_p')[0] for x in mp4filesSliced])

    print('mp4 to mp4 slincing step for : ', position)
    commonElement(mp4filesUnslicedId, mp4filesSlicedId, 'no')
    print('')
    print('')



position = 'close_position'
position =['far_position', 'middle_position', 'close_position']
mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'

for i in position:
    checkFileConversionAviMp4(mainPath, i)

###################################################
# to get and check the file size
###################################################
mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.mp4')
getSize(files)
files = glob.glob(mainPath+'/**/*.avi')
getSize(files)


###################################################
# to move to archive
###################################################
mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.avi')

for i in files:
	archiveDatFct(i)