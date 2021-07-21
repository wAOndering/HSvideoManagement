import glob
import os
import pandas as pd
import numpy as np

mainPath = r'Y:\Sheldon\Highspeed\not_analyzed\WDIL009'
files = glob.glob(mainPath+'/**/*.mp4')


def commonElement(list1, list2, option='dext'):
	'''
	function to identify common element in the list
	option: 'dext' enables to look at the basefilename without the extension useful to check if the files
	were in deed compressed
	'''
	if option == 'dext':
		list1 = [x.split(os.sep)[-1].split('.')[0] for x in list1]
		list2 = [x.split(os.sep)[-1].split('.')[0] for x in list1]

	commonElem = [x for x in list1 if x in list2]

	print('There are', len(commonElem), 'out of', max(len(list1), len(list2)), 'files which are common')

	notcommonElem = []
	if max(len(list1), len(list2)) != len(commonElem):
		notcommonElem = [x for x in list1 if x not in list2]
		# alternatively could use np.setdiff1d(list1, list2)
		print('None common element are:')
		print(notcommonElem)
	else:
		print('No none common element found')

	return notcommonElem



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